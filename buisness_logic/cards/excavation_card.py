from typing import Dict
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from core.containers.resource_container import ResourceContainer
from common.entities.multicombination import Combination
from buisness_logic.actions import *

class ExcavationCard(BaseCard, ResourceContainer):
    
    def __init__(self):
        self._name = "Excavation"
        self._id = 4
        self._level = -1
        self._actions = Combination( 
            ActionCombinationEnum.AndThen,
            takeAccumulatedItemsAction.TakeAccumulatedItemsAction(),
            Combination( 
                ActionCombinationEnum.Or,
                placeATileAction.PlaceATileAction( TileTypeEnum.cavernTunnelTwin ),
                placeATileAction.PlaceATileAction( TileTypeEnum.cavernCavernTwin ) ) )
        
    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        newResources = {ResourceTypeEnum.stone: 1} if self.HasResources() else {ResourceTypeEnum.stone: 2}
        self.GiveResources(newResources)
        
        return self.GetResources()
