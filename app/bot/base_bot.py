from abc import ABC, abstractmethod

from db.base_database import BaseDataBase
from neural_network.base_neural_network import BaseNeuralNetwork

class BaseBot(ABC):
    def __init__(self, token: str, neural_network: BaseNeuralNetwork, db: BaseDataBase) -> None:
        self._token = token
        self._neural_network = neural_network
        self._db = db

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError()