import os

from dotenv import load_dotenv
from pydantic_settings import SettingsConfigDict, BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


## Две функции, которые возращает строки адресса БД для синхронной и асинхронной работы,
# адрес задан в неявном виде через файл .env, таким образом данные нашей БД нельзя украсть

class Settings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_SUPER_USER: str
    DB_SUPER_USER_PASSWORD: str
    DB_PORT: int

    # достаем из .env данные для подключения к нашей БД
    load_dotenv()
    DB_HOST = os.environ.get("DB_HOST")
    DB_NAME = os.environ.get("DB_NAME")
    DB_SUPER_USER = os.environ.get("DB_SUPER_USER")
    DB_SUPER_USER_PASSWORD = os.environ.get("DB_SUPER_USER_PASSWORD")
    DB_PORT = os.environ.get("DB_PORT")

    @property
    def DATABASE_URL_asyncpg(self):
        # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
        return f"postgresql+asyncpg://{self.DB_SUPER_USER}:{self.DB_SUPER_USER_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_pg8000(self):
        # DSN
        # postgresql+psycopg://postgres:postgres@localhost:5432/sa
        return f"postgresql+pg8000://{self.DB_SUPER_USER}:{self.DB_SUPER_USER_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file ='.env') ### ВАЖНО!!!! БЛЯТЬ В ЭТОМ ФАЙЛЕ НЕ ДОЛЖНО
                                                                # БЫТЬ НИ ОДНОЙ ЛИШНЕЙ ПЕРЕМЕННОЙ, ИНАЧЕ ПИЗДА!!!

settings = Settings()

sync_engine = create_engine(
    url = settings.DATABASE_URL_pg8000,
    echo = True,
    pool_size = 5,
    max_overflow = 10
)

session_factory = sessionmaker(sync_engine)