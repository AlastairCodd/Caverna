from abc import abstractmethod, ABC

from common.entities.player import Player
from core.baseClasses.base_effect import BaseEffect


class BasePopulationEffect(BaseEffect, ABC):
    pass


class IncreasePopulationCapacityEffect(BasePopulationEffect):
    def __init__(self, increase_capacity_by: int = 1):
        BaseEffect.__init__(self)
        self._increase_capacity_by = increase_capacity_by

    @property
    def capacity(self) -> int:
        return self._increase_capacity_by


class IncreasePopulationMaximumEffect(BasePopulationEffect):
    def __init__(self, raise_maximum_by: int = 1):
        BaseEffect.__init__(self)
        self._raise_maximum_by = raise_maximum_by

    @property
    def raise_maximum_population_by(self) -> int:
        return self._raise_maximum_by
