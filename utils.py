from datetime import datetime
from typing import Any

from bson import Decimal128


def custom_serializer(obj: Any) -> str:
    """
    Сериализатор для преобразования объектов, которые не могут быть автоматически
    преобразованы в JSON.

    Аргументы:
        obj<Any>: Объект, который необходимо сериализовать.

    Возвращает:
        str: Сериализованный объект.

    Вызывает:
        TypeError: Если тип объекта не поддерживается.
    """
    if isinstance(obj, datetime):  # специальная функция, которая гораздо удобнее проверяет объект на тип данных. Если текущий obj по типу данных равен datetime
        return obj.isoformat()  # верни преобразованый объект в iso формате в строчке
    if isinstance(obj, Decimal128):  # если текущий объект по типу данных - Decimal128
        return str(obj)  # верни его строковое отображение
    raise TypeError(f"Type {obj.__class__.__name__} not serializable")  # если текущий объект не подпадает ни под один из этих типов данных - подними ошибку типа.
