from typing import Any

from cache_storage.user_data import UserData


class CacheStorage(dict):
    def __init__(self) -> None:
        self.__data: dict[int, UserData] = dict()

    def __getitem__(self, __key: int) -> UserData:
        return self.__data[__key]
    
    def __delitem__(self, __key: int) -> None:
        del self.__data[__key]
    
    def create(self, user_id: int) -> None:
        self.__data[user_id] = UserData()

    def get_messages(self, user_id: int) -> list:
        return self.__data[user_id].messages
    
    def add_message(self, user_id: int, message: Any) -> None:
        self.__data[user_id].messages.append(message)

    def pop_message(self, user_id: int) -> None:
        self.__data[user_id].messages.pop()

    def get_question_number(self, user_id: int) -> int:
        return self.__data[user_id].question
    
    def next_question(self, user_id: int) -> None:
        self.__data[user_id].question += 1
