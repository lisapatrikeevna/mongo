import os
from typing import Mapping, Any, List

from dotenv import load_dotenv
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.database import Database
import json

from mongo_connector import MongoConnector
from utils import custom_serializer

load_dotenv()

CONN_STRING: str = os.environ.get("MONGO_CONN_STRING")


def get_apartment_in_manhattan() -> str:
    """
    Функция возвращает квартиры в Манхэттене.

    Мы используем соединение с MongoDB, чтобы найти все квартиры в
    указанной геометрической области Манхэттена.

    Возвращает:
        str: Квартиры в Манхэттене в формате JSON.
    """
    with MongoConnector(CONN_STRING) as mc:  # тут мы входим в контекст класса, который отвечает за подключение к базе данных по строке подключения. Плюс здесь в том, что соединение по завершению контекста будет само закрываться.
        db: Database[Mapping[str, Any]] = mc.client["TEST"]  # здесь мы указываем для клиента, к какой конкретной базе данных мы хотим подключиться для работы. Аналогично команде use TEST; в mongosh
        collection: Collection[Mapping[str, Any]] = db["airbnb"]  # после указания базы нам остаётся указать конкретную коллекцию, в которой хотим работать

        result: Cursor[Mapping[str, Any]] = collection.find({  # после манипуляций выше можем начинать работу с функциями. Они должны быть такими же, как и у mongosh
            "address.location.coordinates": {
                "$geoWithin": {
                    "$geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [-74.00699615478517, 40.70927151739564],
                                [-73.97850036621095, 40.71083299030839],
                                [-73.95858764648439, 40.748557450215635],
                                [-73.93283843994142, 40.79223904263018],
                                [-73.92734527587892, 40.81380923056961],
                                [-73.95000457763673, 40.836151668569975],
                                [-74.00974273681642, 40.75271883902363],
                                [-74.01866912841798, 40.71577741296778],
                                [-74.00699615478517, 40.70927151739564]
                            ]
                        ]
                    }
                }
            }
        }).sort("price", 1).limit(1)  # обратите, пожалуйста, внимание, что в sort() методе не указывается словарь, просто в формате аргументов: что за ключ, порядок сортировки.

        results: List[Mapping[str, Any]] = list(result)

    return json.dumps(  # JSON тут не обязателен на самом деле. Но хотелось, чтобы вам выводилось в консоли более понятно всё.
        results,
        default=custom_serializer,  # этот параметр можно указывать, если в данных есть некие значения, которые просто так JSON не может декодировать. В нашем случае это datetime объекты и Decimal123 тип данных. Для них я написал отдельный кодировщик
        indent=4
    )


def get_first_document_from_airbnb() -> str:
    """
    Функция возвращает первый документ из коллекции airbnb.

    Мы используем соединение с MongoDB, чтобы найти первый документ в
    коллекции airbnb и вернуть его.

    Возвращает:
        str: Первый документ из коллекции airbnb в формате JSON или пустой
        JSON, если коллекция пуста.
    """
    with MongoConnector(CONN_STRING) as mc:
        db: Database[Mapping[str, Any]] = mc.client["TEST"]  #
        collection: Collection[Mapping[str, Any]] = db["airbnb"]

        result: Cursor[Mapping[str, Any]] = collection.find().limit(1)

        document: Mapping[str, Any] = next(result, None)  # для работы с одним объектом прокидываем его в функцию next(), которая на выходе из курсора даст нам Маппируемый объект - наш словарик

        if document is not None:  # если документ мы получим
            return json.dumps(  # выводим его
                document,
                default=custom_serializer,
                indent=4
            )

        return json.dumps({})  # в противном случае возвращаем просто пустой словарик

if "__main__" == __name__:  # если файл является главным, он нигде в импортах не учавствует
    print(get_apartment_in_manhattan())  # запусти какой-то функционал.

    # print(get_first_document_from_airbnb())  # обе функции тут в принтах, так как они содержат в себе return. Если хотим увидеть результат в консоли - бахаем принты.