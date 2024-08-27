from abc import ABC, abstractmethod
from types import TracebackType
from typing import Union


class Connector(ABC):
    """
        Абстрактный базовый класс для подключения к разным сервисам,
        в нашем случае к базам данных.

        Этот класс как шаблон, который можно бедет использовать, чтобы
        создать свои собственные классы для подключения.
        Всё, что нужно, это реализовать эти абстрактные методы
        в своём классе.

        Методы:
        -------
        connect() -> None:
            Метод, где будет описано, как подключаться.

        disconnect() -> None:
            Метод для описания отключения.

        __enter__() -> 'Connector':
            Метод, который позволяет использовать объект в конструкции
            "with". Возвращает сам объект.

        __exit__(
        * **exc_type**: Union[type, None],
        * **exc_value**: Union[BaseException, None],
        * **traceback**: Union[TracebackType, None]) -> None:
            Метод для отключения и обработки ошибок при выходе из конструкции "with".
        """

    @abstractmethod
    def connect(self) -> None:
        """
            Подключение к ресурсу.
            Этот метод нужно будет реализовать в своём классе и описать, как
            именно подключаться к ресурсу (например, базе данных).
        """
        ...

    @abstractmethod
    def disconnect(self) -> None:
        """
        Отключение от ресурса.
        В этом методе описываем, как отключаться от ресурса.
        """
        ...

    @abstractmethod
    def __enter__(self) -> 'Connector':
        """
            Вход в контекстный менеджер.
            Этот метод позволяет использовать объект в "with".
            Обычно здесь подключаемся к ресурсу.

            Возвращает:
                **Connector**: Возвращает самого себя.
        """
        ...

    @abstractmethod
    def __exit__(
            self,
            exc_type: Union[type, None],
            exc_value: Union[BaseException, None],
            traceback: Union[TracebackType, None]) -> None:
        """
            Выход из контекстного менеджера.
            Этот метод нужен для отключения от ресурса при выходе из "with".
            Тут же можно обрабатывать ошибки.

            Аргументы:
                * **exc_type** (Union[type, None]): Тип исключения, если что-то пошло не так.
                * **exc_value** (Union[BaseException, None]): Само исключение, если было.
                * **traceback** (Union[TracebackType, None]): Трассировка стека, если было исключение.
        """
        ...
