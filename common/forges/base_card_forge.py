from abc import ABCMeta, abstractmethod
from typing import List

from core.baseClasses.base_card import BaseCard


class BaseCardForge(metaclass=ABCMeta):
    @abstractmethod
    def is_valid_for_number_of_players(self, number_of_players: int) -> bool:
        pass

    @abstractmethod
    def get_cards(self) -> List[BaseCard]:
        pass


class BaseLevelledCardForge(metaclass=ABCMeta):
    @abstractmethod
    def get_sequential_cards(self) -> List[BaseCard]:
        pass

    def get_additional_cards(self) -> List[BaseCard]:
        return []
