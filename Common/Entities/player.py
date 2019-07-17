from typing import Iterable, Dict
from common.entities.dwarf import Dwarf
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from core.containers.resource_container import ResourceContainer
from core.containers.tile_container import TileContainer

class Player(ResourceContainer, TileContainer):

    def __init__(
        self, 
        id: int, 
        turnIndex: int):
        
        self._id = id
        self._turnIndex = turnIndex
        
        self._dwarves: List[Dwarf] = [ Dwarf(True), Dwarf(True) ]

    def set_turn_index(self, turnIndex: int):
        self._turnIndex = turnIndex
    
    def give_baby_dwarf(self):
        babyDwarf: Dwarf = Dwarf()
        
        self._dwarves.append(babyDwarf)
        
    def get_dwarves(self) -> Iterable[Dwarf]:
        return self._dwarves
        
    def can_take_move(self) -> bool:
        """Determines whether this player can still make a move this turn"""
        isDwarfActive: List[bool] = map(lambda x: not x.get_is_active(), self._dwarves)
        return any(isDwarfActive)
       
    def get_player_response(self, action):
        """Gets a player response for the given action. 
        Implementation left to implementing class -- either from user input, or from analysis of the action value function
        
        Returns relevant information to allow the calling action to change the player or board state based in accordance with the action"""
        raise NotImplementedError()
        
        