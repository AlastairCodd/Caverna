from common.entities.player import Player
from core.baseClasses.base_effect import BaseEffect


class BasePopulationEffect(BaseEffect):
    def Invoke(self, player: Player) -> bool:
        raise NotImplementedError("base population effect class")


class IncreasePopulationCapEffect(BasePopulationEffect):
    def __init__(self, increase_by: int):
        self._increaseBy = increase_by

    def Invoke(self, player: Player) -> bool:
        raise NotImplementedError()


class AllowSixthDwarfEffect(BasePopulationEffect):
    def Invoke(self, player: Player) -> bool:
        raise NotImplementedError()
