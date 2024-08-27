from types import TracebackType
from typing import Union

from pymongo import MongoClient

from connector import Connector


class MongoConnector(Connector):

    def __init__(self, connection_string: str) -> None:
        self.connection_string: str = connection_string
        self.client: Union[MongoClient, None] = None

    def connect(self) -> None:
        self.client: 'MongoClient' = MongoClient(self.connection_string)
        print("Connected to MongoDB...")

    def disconnect(self) -> None:
        if self.client:
            self.client.close()
            print("Disconnected from MongoDB...")

    def __enter__(self) -> 'MongoConnector':
        self.connect()
        return self

    def __exit__(
            self,
            exc_type: Union[type, None],
            exc_value: Union[BaseException, None],
            traceback: Union[TracebackType, None]) -> None:
        self.disconnect()
