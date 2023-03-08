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

    def __format__(self, format_spec):
       text = [
           ("", "you made feed "),
           ("class:count", str(1)),
           ("", " "),
           ("", "dwarf"),
           ("", " with "),
       ]

       for (i, (resource, amount)) in enumerate(self._substitute_with.items()):
           text.append(("class:count", str(amount)))
           text.append(("", " "))
           text.append(("", resource.name))
           if i != len(self._substitute_with) - 1:
               text.append(("", ", "))

       if format_spec == "pp":
          return text
       if format_spec.isspace():
          return "".join(e[1] for e in text)
       raise ValueError("format parameter must be 'pp' or whitespace/empty")


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
            conditional: Callable[[BasePlayerRepository], int],
            per_condition_repr: str) -> None:
        if conditional is None:
            raise ValueError("Conditional may not be None")
        if per_condition_repr is None or per_condition_repr.isspace():
            raise ValueError("per condition representation may not be null or whitespace")
        self._conditional: Callable[[BasePlayerRepository], int] = conditional
        self._per_condition_repr: str = per_condition_repr

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

    def __format__(self, format_spec):
       text = [
           ("", "discount when feeding "),
           ("", "dwarfs"),
           ("", " of "),
           ("class:count", self._per_condition_repr),
       ]

       if format_spec == "pp":
          return text
       if format_spec.isspace():
          return "".join(e[1] for e in text)
       raise ValueError("format parameter must be 'pp' or whitespace/empty")
