from abc import ABC, abstractmethod

from pysc2.lib.named_array import NamedDict

class Game(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def user_content(self, observation: NamedDict, available_actions: list[str], reward:int) -> str:
        pass

    @abstractmethod
    def system_content(self) -> str:
        pass