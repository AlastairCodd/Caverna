from typing import Dict, Iterable
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum
from core.baseClasses.base_action import BaseAction
from common.entities.dwarf import Dwarf

class BaseCard(object):
    _name: str = "Uninitialised"
    _id: int = -1
    _level: int = -1
    _actions: Iterable[BaseAction] = []
    _actionCombinationType: ActionCombinationEnum = ActionCombinationEnum.EitherOr
    _currentItems: Dict[ResourceTypeEnum, int] = {}
    
    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        raise NotImplementedError("abstract base card class")
        
    def ActivateCard(
            self, 
            player,
            dwarf: Dwarf ) -> bool:
        return False