from abc import ABCMeta, abstractmethod
from typing import List, Dict, Callable

from core.baseClasses.base_effect import BaseEffect
from core.enums.caverna_enums import ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository


class BaseFoodEffect(BaseEffect, metaclass=ABCMeta):
    pass


class FoodPerDwarfEffect(BaseFoodEffect, metaclass=ABCMeta):
    @abstractmethod
    def invoke(self, resources_per_dwarf: List[Dict[ResourceTypeEnum, int]]) -> None:
        pass


class SubstituteFoodForDwarfEffect(FoodPerDwarfEffect):
    def __init__(
            self,
            substitute_with: Dict[ResourceTypeEnum, int]) -> None:
        if substitute_with is None:
            raise ValueError("Cannot substitute with nothing")
        self._substitute_with: Dict[ResourceTypeEnum, int] = substitute_with

    def invoke(
            self,
            resources_per_dwarf: List[Dict[ResourceTypeEnum, int]]) -> None:

        ordered_resources_per_dwarf: List[Dict[ResourceTypeEnum, int]] = sorted(
            filter(
                lambda x: len(x) == 1 and ResourceTypeEnum.food in x,
                resources_per_dwarf),
            key=lambda x: x[ResourceTypeEnum.food],
            reverse=True)
        if len(ordered_resources_per_dwarf) > 0:
            value_to_process: Dict[ResourceTypeEnum, int] = ordered_resources_per_dwarf[0]
            value_to_process.clear()
            value_to_process.update(self._substitute_with)


class FoodGlobalEffect(BaseFoodEffect, metaclass=ABCMeta):
    @abstractmethod
    def invoke(
            self,
            resources: Dict[ResourceTypeEnum, int],
            player: BasePlayerRepository) -> None:
        pass


class DiscountEffect(FoodGlobalEffect):
    def __init__(
            self,
            conditional: Callable[[BasePlayerRepository], int]) -> None:
        if conditional is None:
            raise ValueError("Conditional may not be None")
        self._conditional: Callable[[BasePlayerRepository], int] = conditional

    def invoke(
            self,
            resources: Dict[ResourceTypeEnum, int],
            player: BasePlayerRepository) -> None:
        if resources is None:
            raise ValueError("Resources may not be None")
        if player is None:
            raise ValueError("Player may not be None")

        if ResourceTypeEnum.food in resources:
            discount_amount: int = self._conditional(player)
            resources[ResourceTypeEnum.food] -= min(resources[ResourceTypeEnum.food], discount_amount)