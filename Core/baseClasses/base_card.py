from typing import Dict, Iterable
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum
from core.baseClasses.base_action import BaseAction
from common.entities.dwarf import Dwarf

class BaseCard(object):

    def __init__(self):
        self._name: str = "Uninitialised"
        self._id: int = -1
        self._level: int = -1
        self._actions: None
        self._isActive = False
        self._isAvailable = False
    
    def activate_card(
            self, 
            player,
            dwarf: Dwarf ) -> bool:
        if player is None: raise ValueError("player")    
        if dwarf is None: raise ValueError("dwarf")    
        if dwarf.get_is_active: raise ValueError("dwarf cannot already be active")
        
        actionChoices: Iterable[BaseAction] = []
        for action in self._actions:
            action.invoke(player, self)
        dwarf.set_active(self)
        
    def make_available(self):
        self._isAvailable = True
        
    def get_level(self):
        return self._level