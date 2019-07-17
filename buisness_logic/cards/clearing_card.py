from typing import Dict
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from core.containers.resource_container import ResourceContainer
from common.entities.multicombination import Combination
from buisness_logic.actions import *

class ClearingCard(BaseCard, ResourceContainer):
    
    def __init__(self):
        self._name = "Clearing"
        self._id = 0
        self._level = -1
        self._actions = Combination( 
            ActionCombinationEnum.AndThenOr,
            takeAccumulatedItemsAction.TakeAccumulatedItemsAction(),
            placeATileAction.PlaceATileAction( TileTypeEnum.meadowFieldTwin ) )
        
    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        self.GiveResource( ResourceTypeEnum.wood, 2 )
        
        return self.GetResources()
