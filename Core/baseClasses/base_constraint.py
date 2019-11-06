from abc import ABC, abstractmethod
from typing import List

from core.baseClasses.base_action import BaseAction


class BaseConstraint(ABC):
    @abstractmethod
    def passes_condition(self, actions: List[BaseAction]) -> bool:
        pass
