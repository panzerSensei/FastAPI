import os
import time
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List

from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import select
import shutil
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
import redis
from celery import Celery
import pytesseract
from PIL import Image

from DB_models import Base_Model, Table_documents, Table_documents_text, create_Tables_ORM
from DB_CREATE import insert_data_DB
from DB_config import session_factory

## объявляем редис и некоторые параметры его работы
r = redis.Redis(host='redis', port=6379, decode_responses=True)

## при запуске приложения происзодит подключение к редис для Кэширования некоторых результатов запросов, например,
# которые будут часто запрашивать пользователи
@asynccontextmanager
async def lifespan(app: FastAPI):
    # redis = aioredis.from_url("redis://[::1]:6379/0", encoding="utf8", decode_respones=True)
    FastAPICache.init(RedisBackend(r), prefix="fastapi-cache")
    yield

app = FastAPI(
    title='Mebel Store2',
    lifespan=lifespan
)


# объявляем путь хранения файлов
app.mount("/media", StaticFiles(directory='media'), name='media')

@app.post('/Create_DB_example')
async def create_DB():
    """
    Ручка чтобы сгенерировать БДшку для теста
    """

    insert_data_DB()

    return{
        "status": 200,
        "DataBase created": "GZ"
    }


@app.delete('/Delete/All_Data')
async def delete_DB():
    """
    Ручка для очистки БД от всех записей и обновления индексов с нуля
    """

    create_Tables_ORM()

    return {
        "status": 200,
        "DataBase purged": "GZ"
    }

@app.post('/document/upload')
async def upload_file(upload_file: UploadFile = File(...)):
    """
    Загружает файл в директорию хранения медиа файлов,
    \nтакже добавляет связанные с файлом записи в базе данных:
    \nесли это файл расширения .txt в поле "текст" будет добавлена
    \nпервая строка из файла
    \nВозвращает -  данные о файле: общие данные включая размер, новый путь хранения, тип файла
    """
    upload_file.filename = upload_file.filename.lower()
    path = f'media/{upload_file.filename}'

    with open(path, 'wb+') as buffer: ## загрузка файла на диск
        shutil.copyfileobj(upload_file.file, buffer)

    # делаем записи в БД, если этот txt файл, то пишем первую строку, если нет, то просто "not text type"

        with open(path, 'r', encoding="utf-8") as file:
            with session_factory() as session:
                document1 = Table_documents(
                    psth=path,
                    date=datetime.now()
                )
                if upload_file.content_type == 'text/plain':
                    str_from_file = file.read()
                    document_text1 = Table_documents_text(
                        text=file.readline(),
                        parent=document1
                    )
                else:
                    str_from_file = 'Not text type'
                    document_text1 = Table_documents_text(
                        text='Not text type',
                        parent=document1
                    )

            session.add_all([document1, document_text1])
            session.flush()
            session.refresh(document1)
            new_id = document1.ID_doc
            session.commit()

    return{
        "file": upload_file,
        "filename": path,
        "type": upload_file.content_type,
        "text from file": str_from_file,
        "new insert id is": new_id
    }


@app.delete('/document/delete')
async def delete_file(file_id: int):
    """
    Удаляет по указанному id файл из директории хранения медиа файлов,
    \nтакже удаляет связанные с файлом записи в базе данных
    \nВозвращает - успешный статус удаления 200 и путь по которому был удален файл
    """
    with session_factory() as session:
        query = select(Table_documents.psth).where(Table_documents.ID_doc == file_id)
        res = session.execute(query)
        a = res.one()
        path = a[0]
        # производим удаление файла при его наличии
        if os.path.exists(path):
            os.remove(path)
            file_status = f'deleted {path}'
            # удаляем запись из БД каскадно, каскадность прописана в моделях таблиц
            stmt = session.query(Table_documents).filter(Table_documents.ID_doc == file_id).first()
            session.delete(stmt)
            session.commit()
            Status = 200
        else:
            file_status = f'{path} dont exist in'
            Status = 201

    return {
        "Status": Status,
        "file status": file_status
        }


@app.get("/text")
@cache(expire=60)
async def get_doc_text(doc_id: int):
    """
    По введенному id находит текст файла и выдает пользователю
    \nВозвращает - строку
    """
    with session_factory() as session:
        query = select(Table_documents_text.text).where(Table_documents_text.ID_doc == doc_id)
        res = session.execute(query)
        a = res.one()
        result = a[0]
        time.sleep(2) ## симулируем долгую работу ф-ии, чтобы потом после кэширования видеть разницу в скорости результата
    return result

celery = Celery('analyse')
celery.config_from_object('settings', namespace='CELERY')
celery.conf.broker_connection_retry_on_startup = True

pytesseract_config = r'-l rus --oem 3 --psm 1'

@celery.task
def get_image_text(doc_id: int):
    with session_factory() as session:
        query = select(Table_documents.psth).where(Table_documents.ID_doc == doc_id)
        res = session.execute(query)
        a = res.one()
        root = a[0]

        if os.path.exists(root):
            img = Image.open(root)
            try:
                text = pytesseract.image_to_string(img, config=pytesseract_config)
            except:
                text = "It's not image file, cant recognize text via Tesseract OCR"
            table_documents1 = session.get(Table_documents, doc_id)
            table_documents1.children.text = text
            session.commit()

        else:
            text = "There's no image for this ID"

    return str(f'{text} - {root}')

@app.patch('/document/analyse')
async def analyse_doc(file_id: int):
    """
    По введенному id находит файл, который должен являться изображением с текстом,
    \nраспознает текст с помощью OCR_Tesserct и возвращает пользователю текст, также
    \nделает запись в поле "text" в БД по указанному id
    \nВозвращает - строку (распознанный текст)
    """
    result1 = get_image_text.delay(file_id)
    text = result1.get(timeout=1000)
    return text


@app.get('/application/Status')
async def application_status():
    """
    Быстрая проверка ответа от сервера, если есть status: true
    приложение работает нормально
    """
    return {
        'aboba': False,
        'status': True
    }