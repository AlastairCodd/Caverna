from typing import Dict
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from core.containers.resource_container import ResourceContainer
from common.entities.multicombination import Combination
from buisness_logic.actions import *

class FenceBuildingCard(BaseCard, ResourceContainer):
    
    def __init__(self):
        self._name = "Fence Building"
        self._id = 5
        self._level = -1
        self._actions = Combination(
            ActionCombinationEnum.AndThen,
            takeAccumulatedItemsAction.TakeAccumulatedItemsAction(),
            Combination(
                ActionCombinationEnum.AndOr,
                Combination(
                    ActionCombinationEnum.AndThen,
                    payAction.PayAction( {ResourceTypeEnum.wood, 2} ),
                    placeATileAction.PlaceATileAction( TileTypeEnum.pastureTwin ) ),
                Combination(
                    ActionCombinationEnum.AndThen,
                    payAction.PayAction( {ResourceTypeEnum.wood, 4} ),
                    placeATileAction.PlaceATileAction( TileTypeEnum.pastureTwin )
                ) ) )
        
    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        newResources = {ResourceTypeEnum.wood: 1} if self.HasResources() else {ResourceTypeEnum.wood: 2}
        self.GiveResources(newResources)
        
        return self.GetResources()
