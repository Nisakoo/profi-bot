from typing import Any, Coroutine
import aiosqlite

from db.base_database import BaseDataBase


class Sqlite3DataBase(BaseDataBase):
    def __init__(self, **kwargs) -> None:
        self._database_file = kwargs["filename"]

    async def connect(self) -> None:
        pass
    
    async def close(self) -> None:
        pass
    
    async def insert(self, **kwargs) -> None:
        pass