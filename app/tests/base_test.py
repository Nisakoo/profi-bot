from typing import Any
from abc import ABC, abstractmethod, abstractproperty


class BaseTest(ABC):
    @abstractmethod
    def __init__(self, short_name, **kwargs) -> None:
        raise NotImplementedError()
    
    @abstractproperty
    def name(self) -> str:
        raise NotImplementedError()
    
    @abstractproperty
    def short_name(self) -> str:
        raise NotImplementedError()
    
    @abstractproperty
    def description(self) -> str:
        raise NotImplementedError()
    
    @abstractproperty
    def questions_count(self) -> int:
        raise NotImplementedError()
    
    @abstractmethod
    def current_question(self, **kwargs) -> int:
        raise NotImplementedError()
    
    @abstractmethod
    def start_test(self, **kwargs) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def next_question(self, **kwargs) -> str:
        raise NotImplementedError()
    
    @abstractmethod
    def show_result(self, **kwargs) -> str:
        raise NotImplementedError()
    
    @abstractmethod
    def is_ended(self, **kwargs) -> str:
        raise NotImplementedError()
    
    @abstractmethod
    def end_test(self, **kwargs) -> None:
        raise NotImplementedError()