from abc import ABC, abstractmethod


class BaseDataBase(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    async def connect(self) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    async def insert(self, **kwargs) -> None:
        raise NotImplementedError()