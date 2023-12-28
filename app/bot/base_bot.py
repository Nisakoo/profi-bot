from abc import ABC, abstractmethod

from db.base_database import BaseDataBase

class BaseBot(ABC):
    def __init__(self, token: str, tests: list, db: BaseDataBase) -> None:
        self._token = token
        self._tests = tests
        self._db = db

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError()