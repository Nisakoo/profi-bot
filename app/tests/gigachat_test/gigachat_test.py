from tests.base_test import BaseTest
from neural_network.base_neural_network import BaseNeuralNetwork
from neural_network.gigachat.gigachat import GigaChatNeuralNetwork
from cache_storage.cache_storage import CacheStorage
from tests.gigachat_test.description import *


class GigaChatTest(BaseTest):
    def __init__(self, short_name, **kwargs) -> None:
        self._ai: BaseNeuralNetwork = kwargs["ai"]
        self._short_name = short_name

        assert(type(self._ai) == GigaChatNeuralNetwork)

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

        if self._data.get_question_number(user_id) > 1:
            self._data.add_message(user_id, self._ai.user_msg(message))

        response = await self._ai.ask_question(self._data.get_messages(user_id))
        self._data.add_message(user_id, self._ai.agent_msg(response))

        self._data.next_question(user_id)

        return QUESTION_TEMPLATE.format(
            questions_count=QUESTIONS_COUNT,
            question=self._data.get_question_number(user_id)-1,
            question_content=response
        )
    
    async def show_result(self, **kwargs) -> str:
        user_id = kwargs["user_id"]
        message = kwargs["message"]

        self._data.add_message(user_id, self._ai.user_msg(message))
        response = await self._ai.ask_result(self._data.get_messages(user_id))
        
        return RESULT_TEMPLATE.format(
            result_content=response
        )
    
    def is_ended(self, **kwargs) -> bool:
        return self._data.get_question_number(kwargs["user_id"]) > QUESTIONS_COUNT
    
    def end_test(self, **kwargs) -> None:
        del self._data[kwargs["user_id"]]