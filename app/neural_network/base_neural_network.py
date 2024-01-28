from typing import Any
from abc import ABC, abstractmethod


class BaseNeuralNetwork(ABC):
    def __init__(self, auth_key: str) -> None:
        self._auth_key = auth_key

    @abstractmethod
    async def ask_question(self, messages: list) -> str:
        raise NotImplementedError()
    
    @abstractmethod
    async def ask_comment(self, message: str) -> str:
        raise NotImplementedError()
    
    @abstractmethod
    async def ask_result(self, messages: list) -> str:
        raise NotImplementedError()
    
    @abstractmethod
    def user_msg(self, prompt: str) -> Any:
        raise NotImplementedError()
    
    @abstractmethod
    def agent_msg(self, prompt: str) -> Any:
        raise NotImplementedError()