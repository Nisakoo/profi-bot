from typing import Any

from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

from neural_network.base_neural_network import BaseNeuralNetwork

from neural_network.constants.prompts import *


class GigaChatNeuralNetwork(BaseNeuralNetwork):
    def __init__(self, auth_key: str) -> None:
        super().__init__(auth_key)

        self._gigachat = GigaChat(
            credentials=self._auth_key,
            verify_ssl_certs=False,
            temperature=1.0
        )

    async def ask_question(self, messages: list) -> str:
        prompts = messages.copy()

        prompts.insert(0, SystemMessage(content=ASK_QUESTION_SYSTEM_PROMPT))
        prompts.insert(1, HumanMessage(content=ASK_NEXT_QUESTION_PROMPT))

        return (await self._gigachat.ainvoke(prompts)).content
    
    async def ask_result(self, messages: list) -> str:
        prompts = messages.copy()
        prompts.insert(0, SystemMessage(content=SHOW_RESULT_SYSTEM_PROMPT))

        prompts = [i for i in prompts if type(i) != AIMessage]

        return (await self._gigachat.ainvoke(prompts)).content
    
    def user_msg(self, prompt: str) -> Any:
        return HumanMessage(content=prompt)
    
    def agent_msg(self, prompt: str) -> Any:
        return AIMessage(content=prompt)