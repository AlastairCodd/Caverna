from typing import Iterable, List, Dict
from common.entities.dwarf import Dwarf
from core.containers.resource_container import ResourceContainer
from core.containers.tile_container import TileContainer
from core.enums.caverna_enums import ResourceTypeEnum


class Player(TileContainer, ResourceContainer):

    def __init__(self, player_id: int, turnIndex: int):
        self._id: int = player_id
        self._turnIndex: int = turnIndex

        self._dwarves: List[Dwarf] = [Dwarf(True), Dwarf(True)]

        TileContainer.__init__(self)
        ResourceContainer.__init__(self)

    @property
    def id(self) -> int:
        return self._id

    @property
    def dwarves(self) -> List[Dwarf]:
        return list(self._dwarves)

    def set_turn_index(self, turnIndex: int):
        self._turnIndex = turnIndex

    def give_baby_dwarf(self):
        baby_dwarf: Dwarf = Dwarf()

        self._dwarves.append(baby_dwarf)

    def can_take_move(self) -> bool:
        """Determines whether this player can still make a move this turn"""
        is_dwarf_active: Iterable[bool] = map(lambda x: not x.is_active(), self._dwarves)
        return any(is_dwarf_active)

    def get_player_choice(self, action):
        """Gets a player response for the given action. 
        Implementation left to implementing class -- either from user input, or from analysis of the action value function
        
        Returns relevant information to allow the calling action to change the player or board state based in accordance with the action"""
        raise NotImplementedError()

    def start_new_turn(self):
        for dwarf in self._dwarves:
            dwarf.make_adult()
