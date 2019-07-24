from typing import Dict, Iterable
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum
from core.baseClasses.base_action import BaseAction
from common.entities.dwarf import Dwarf
from common.services.conditional_service import ConditionalService

class BaseCard(object):

    def __init__(self):
        self._name: str = "Uninitialised"
        self._id: int = -1
        self._level: int = -1
        self._actions: None
        self._isActive = False
    
    def activate_card(
            self, 
            player,
            dwarf: Dwarf ) -> bool:
        if player is None: raise ValueError("player")    
        if dwarf is None: raise ValueError("dwarf")    
        if dwarf.get_is_active: raise ValueError("dwarf cannot already be active")
        
        conditional_service = ConditionalService()
        
        actionChoices: Iterable[BaseAction] = ConditionalService.get_possible_choices( self._actions )
        
        player.get_player_choice

        for action in self._actions:
            action.invoke(player, self)
        dwarf.set_active(self)
        
    def get_level(self):
        return self._level
        
    def is_active(self):
        return self._isActive;
        
    def is_available(self):
        return not self._isActive
        
    def make_available(self):
        self._isActive = True
