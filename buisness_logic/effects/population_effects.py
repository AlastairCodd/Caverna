from abc import abstractmethod, ABC

from common.entities.player import Player
from core.baseClasses.base_effect import BaseEffect


class BasePopulationEffect(ABC, BaseEffect):
    def __init__(self, ):
        pass


class IncreasePopulationCapEffect(BasePopulationEffect):
    def __init__(self, increase_by: int):
        self._increaseBy = increase_by

    @property
    def increase_by(self) -> int:
        return self._increaseBy


class AllowSixthDwarfEffect(BasePopulationEffect):
    def __init__(self):
        BaseEffect.__init__(self)
