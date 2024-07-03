from DB_models import Table_documents, Table_documents_text
from DB_config import sync_engine, session_factory

def insert_data_DB():
    with session_factory() as session:
        document1 = Table_documents(
            psth='C:\\Users\JOGU\Desktop\PhythonProject\FastAPI\docs\А.А.Ахматова - Реквием .txt',
            date='1961-01-01T18:00:00'
        )
        document2 = Table_documents(
            psth='C:\\Users\JOGU\Desktop\PhythonProject\FastAPI\docs\А.А.Блок - Ночь, улица, фонарь, аптека.txt',
            date='1912-01-01T18:00:00'
        )
        document3 = Table_documents(
            psth='C:\\Users\JOGU\Desktop\PhythonProject\FastAPI\docs\А.С.Пушкин_Она.txt',
            date='1817-01-01T18:00:00'
        )
        document4 = Table_documents(
            psth='C:\\Users\JOGU\Desktop\PhythonProject\FastAPI\docs\М.Ю.Лермонтов - Тучи.txt',
            date='1840-01-01T18:00:00'
        )
        document5 = Table_documents(
            psth='C:\\Users\JOGU\Desktop\PhythonProject\FastAPI\docs\Ф.И.Тютчев - Есть в осени первоначальной.txt',
            date='1857-01-01T18:00:00'
        )
        documents_text1 = Table_documents_text(
            ID_doc=1,
            text='Нет, и не под чуждым небосводом,\nИ не под защитой чуждых крыл, —\nЯ была тогда с моим народом,\nТам, где мой народ, к несчастью, был.'
        )
        documents_text2 = Table_documents_text(
            ID_doc=2,
            text='Ночь, улица, фонарь, аптека,\nБессмысленный и тусклый свет.\nЖиви еще хоть четверть века —\nВсё будет так. Исхода нет.\n\nУмрёшь — начнёшь опять сначала\nИ повторится всё, как встарь:\nНочь, ледяная рябь канала,\nАптека, улица, фонарь.'
        )
        documents_text3 = Table_documents_text(
            ID_doc=3,
            text='«Печален ты; признайся, что с тобой».\n— Люблю, мой друг! — «Но кто ж тебя пленила?»\n— Она.— «Да кто ж? Глидера ль, Хлоя, Лила?»\n— О, нет! — «Кому ж ты жертвуешь душой?»\n— Ах! ей! — «Ты скромен, друг сердечный!\nНо почему ж ты столько огорчен?\nИ кто виной? Супруг, отец, конечно…»\n— Не то, мой друг! — «Но что ж!» — Я ей не он.'
        )
        documents_text4 = Table_documents_text(
            ID_doc=4,
            text='Тучки небесные, вечные странники!\nСтепью лазурною, цепью жемчужною\nМчитесь вы, будто как я же, изгнанники\nnС милого севера в сторону южную.\n\nКто же вас гонит: судьбы ли решение?\nЗависть ли тайная? злоба ль открытая?\nИли на вас тяготит преступление?\nИли друзей клевета ядовитая?\n\n\nНет, вам наскучили нивы бесплодные…\nЧужды вам страсти и чужды страдания;\nВечно холодные, вечно свободные,\nНет у вас родины, нет вам изгнания.'
        )
        documents_text5 = Table_documents_text(
            ID_doc=5,
            text='Есть в осени первоначальной\nКороткая, но дивная пора —\nВесь день стоит как бы хрустальный,\nИ лучезарны вечера…\n\n\nГде бодрый серп гулял и падал колос,\nТеперь уж пусто все — простор везде, —\nЛишь паутины тонкий волос\nБлестит на праздной борозде…\n\n\nПустеет воздух, птиц не слышно боле,\nНо далеко еще до первых зимних бурь —\nИ льется чистая и теплая лазурь\nНа отдыхающее поле…'
        )
        session.add_all([document1, document2, document3, document4, document5])
        session.add_all([documents_text1, documents_text2, documents_text3, documents_text4, documents_text5])
        session.commit()