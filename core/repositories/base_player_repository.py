from abc import ABCMeta
from typing import List, Iterable

from common.entities.dwarf import Dwarf
from core.baseClasses.base_tile_container_default import BaseTileContainerDefault
from core.containers.resource_container import ResourceContainer
from core.containers.tile_container import TileContainer


class BasePlayerRepository(TileContainer, ResourceContainer, metaclass=ABCMeta):
    def __init__(
            self,
            player_id: int,
            turn_index: int,
            tile_container_default: BaseTileContainerDefault) -> None:
        self._id: int = player_id
        self._turnIndex: int = turn_index

        self._dwarves: List[Dwarf] = [Dwarf(True), Dwarf(True)]

        TileContainer.__init__(self, tile_container_default)
        ResourceContainer.__init__(self)

    @property
    def id(self) -> int:
        return self._id

    @property
    def dwarves(self) -> List[Dwarf]:
        return list(self._dwarves)

    @property
    def turn_index(self) -> int:
        return self._turnIndex

    def set_turn_index(self, turn_index: int):
        self._turnIndex = turn_index

    def give_baby_dwarf(self) -> None:
        baby_dwarf: Dwarf = Dwarf()

        self._dwarves.append(baby_dwarf)

    @property
    def can_take_move(self) -> bool:
        """Determines whether this player can still make a move this turn"""
        is_dwarf_active: Iterable[bool] = map(lambda x: not x.is_active(), self._dwarves)
        return any(is_dwarf_active)

    def start_new_turn(self):
        for dwarf in self._dwarves:
            dwarf.make_adult()
