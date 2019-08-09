from typing import Dict
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum
from core.containers.resource_container import ResourceContainer
from common.entities.multicombination import Combination
from buisness_logic.actions import *

class RubyMiningCard(BaseCard, ResourceContainer):
    
    def __init__(self):
        BaseCard.__init__(
            self, "Ruby Mining", 33, 4,
            Combination(
                ActionCombinationEnum.AndThenOr,
                takeAccumulatedItemsAction.TakeAccumulatedItemsAction(),
                buyFromMarketAction.BuyFromMarketAction()  ))
            
    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        newResources = {ResourceTypeEnum.ruby: 1} if self.HasResources() else {ResourceTypeEnum.ruby: 2}
        self.GiveResources(newResources)
        
        return self.GetResources()
