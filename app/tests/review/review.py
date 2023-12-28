from tests.base_test import BaseTest
from tests.review.description import *
from cache_storage.cache_storage import CacheStorage


class Review(BaseTest):
    def __init__(self, short_name, **kwargs) -> None:
        self._short_name = short_name
        self._data: CacheStorage = CacheStorage()

    @property
    def name(self) -> str:
        return TEST_NAME
    
    @property
    def short_name(self) -> str:
        return self._short_name
    
    @property
    def description(self) -> str:
        return TEST_DESCRIPTION
    
    @property
    def questions_count(self) -> int:
        return QUESTIONS_COUNT
    
    def current_question(self, **kwargs) -> int:
        return self._data.get_question_number(kwargs["user_id"])

    def start_test(self, **kwargs) -> None:
        user_id = kwargs["user_id"]
        self._data.create(user_id)

    async def next_question(self, **kwargs) -> str:
        user_id = kwargs["user_id"]
        message = kwargs["message"]

        self._data.next_question(user_id)

        return QUESTION_TEXT
    
    async def show_result(self, **kwargs) -> str:
        user_id = kwargs["user_id"]
        message = kwargs["message"]
        
        return RESULT_TEXT
    
    def is_ended(self, **kwargs) -> bool:
        return self._data.get_question_number(kwargs["user_id"]) > QUESTIONS_COUNT
    
    def end_test(self, **kwargs) -> None:
        del self._data[kwargs["user_id"]]