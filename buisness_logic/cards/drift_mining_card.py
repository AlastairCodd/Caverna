from typing import Dict
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from core.containers.resource_container import ResourceContainer
from common.entities.multicombination import Combination
from buisness_logic.actions import *

class DriftMiningCard(BaseCard, ResourceContainer):
    
    def __init__(self):
        self._name = "Drift Mining"
        self._id = 2
        self._level = -1
        self._actions = Combination( 
            ActionCombinationEnum.AndThen,
            takeAccumulatedItemsAction.TakeAccumulatedItemsAction(),
            placeATileAction.PlaceATileAction( TileTypeEnum.cavernTunnelTwin ) )
        
    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        self.GiveResource( ResourceTypeEnum.stone, 2 )
        
        return self.GetResources()
