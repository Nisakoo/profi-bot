from typing import Any

from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

from neural_network.base_neural_network import BaseNeuralNetwork


class GigaChatNeuralNetwork(BaseNeuralNetwork):
    def __init__(self, auth_key: str) -> None:
        super().__init__(auth_key)

        self._gigachat = GigaChat(
            credentials=self._auth_key
        )

    async def ask_question(self, messages: list) -> str:
        raise NotImplementedError("Добавить systeam message для ask_question")

        return (await self._chat.ainvoke(messages)).content
    
    async def ask_result(self, messages: list) -> str:
        raise NotImplementedError("Добавить systeam message для ask_result")

        return (await self._chat.ainvoke(messages)).content
    
    def user_msg(self, prompt: str) -> Any:
        return HumanMessage(content=prompt)
    
    def agent_msg(self, prompt: str) -> Any:
        return AIMessage(content=prompt)