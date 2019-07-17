from typing import Dict
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum
from core.containers.resource_container import ResourceContainer
from common.entities.multicombination import Combination
from buisness_logic.actions import *

class StartingPlayerCard(BaseCard, ResourceContainer):
    
    def __init__(self):
        self._name = "Starting Player"
        self._id = 17
        self._level = -1
        self._actions = Combination(
            ActionCombinationEnum.AndThen,
            takeAccumulatedItemsAction.TakeAccumulatedItemsAction(),
            Combination(
                ActionCombinationEnum.AndThen,
                becomeStartingPlayerAction.BecomeStartingPlayerAction(),
                receiveAction.ReceiveAction( {ResourceTypeEnum.ruby, 1} ) ) )
        
    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        self.GiveResource( ResourceTypeEnum.food, 1 )
        
        return self.GetResources()
