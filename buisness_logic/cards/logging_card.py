from typing import Dict
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum
from core.containers.resource_container import ResourceContainer
from common.entities.multicombination import Combination
from buisness_logic.actions import *

class LoggingCard(BaseCard, ResourceContainer):
    
    def __init__(self):
        self._name = "Logging"
        self._id = 13
        self._level = -1
        self._actions = Combination(
            ActionCombinationEnum.AndThenOr,
            takeAccumulatedItemsAction.TakeAccumulatedItemsAction(),
            goOnAnExpeditionAction.GoOnAnExpeditionAction( 1 ) )
        
    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        self.GiveResource( ResourceTypeEnum.wood, 3 )
        
        return self.GetResources()
