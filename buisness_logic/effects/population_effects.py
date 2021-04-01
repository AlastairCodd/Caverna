from abc import ABCMeta

from core.baseClasses.base_effect import BaseEffect


class BasePopulationEffect(BaseEffect, metaclass=ABCMeta):
    pass


class IncreasePopulationCapacityEffect(BasePopulationEffect):
    def __init__(self, increase_capacity_by: int = 1):
        self._increase_capacity_by = increase_capacity_by

    @property
    def capacity(self) -> int:
        return self._increase_capacity_by

    def __str__(self) -> str:
        dwarf_readable: str = "dwarves" if self._increase_capacity_by > 1 else "dwarf"
        result: str = f"Room for {self._increase_capacity_by} {dwarf_readable}"
        return result


class IncreasePopulationMaximumEffect(BasePopulationEffect):
    def __init__(self, raise_maximum_by: int = 1):
        self._raise_maximum_by = raise_maximum_by

    @property
    def raise_maximum_population_by(self) -> int:
        return self._raise_maximum_by

    def __str__(self) -> str:
        result: str = f"Increase population cap by {self._raise_maximum_by}"
        return result
