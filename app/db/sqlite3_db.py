from typing import Any
from datetime import datetime
import aiosqlite

from db.base_database import BaseDataBase


class Sqlite3DataBase(BaseDataBase):
    def __init__(self, **kwargs) -> None:
        self._database_file = kwargs["filename"]

    async def connect(self) -> None:
        self._connection = await aiosqlite.connect(self._database_file)
        await self._create_table()
    
    async def close(self) -> None:
        await self._connection.close()
    
    async def insert(self, **kwargs) -> None:
        await self._connection.execute("""INSERT INTO events
                                (user_id, date, event, message) VALUES(?, ?, ?, ?)""",
                                (kwargs["user_id"], datetime.now(), kwargs["event"], kwargs["message"])
        )
        await self._connection.commit()

    async def _create_table(self) -> None:
        await self._connection.execute("""CREATE TABLE IF NOT EXISTS events
                          (id INTEGER PRIMARY KEY, user_id INTEGER,
                          date DATETIME, event VARCHAR(32), message TEXT);"""
        )