from abc import ABC, abstractmethod
from typing import List

from core.baseClasses.base_action import BaseAction


class BaseConstraint(ABC):
    @abstractmethod
    def passes_condition(self, actions: List[BaseAction]) -> bool:
        pass

    @abstractmethod
    def get_index_of_first_action_which_fails_constraint(self, actions: List[BaseAction]) -> int:
        """Gets the index of the first index for which this constraint is not valid: returns -1 if is valid for all"""
        return -1
