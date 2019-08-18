from abc import abstractmethod, ABC
from typing import Dict
from core.enums.caverna_enums import ResourceTypeEnum


class BaseAction(object, ABC):

    @abstractmethod
    def invoke(
            self,
            player,
            accumulated_items: Dict[ResourceTypeEnum, int]) -> bool:
        raise NotImplementedError("abstract base action class")

    @abstractmethod
    def new_turn_reset(self):
        pass
