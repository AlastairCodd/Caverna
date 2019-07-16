from typing import Dict
from core.baseClasses.base_card import BaseCard
from core.enums.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum
from core.containers.resource_container import ResourceContainer
from common.entities.multicombination import Combination
from buisness_logic.actions import *

class ForestExplorationCard(BaseCard, ResourceContainer):
	
	def __init__(self):
		self._name = "Forest Exploration"
		self._id = 6
		self._level = -1
		self._actions = Combination(
			ActionCombinationEnum.AndThen,
			takeAccumulatedItemsAction.TakeAccumulatedItemsAction(),
			receiveAction.ReceiveAction( {ResourceTypeEnum.food, 2} ) )
		
	def RefillAction(self) -> Dict[ResourceTypeEnum, int]:
		newResources = {ResourceTypeEnum.wood: 1} if self.HasResources() else {ResourceTypeEnum.wood: 2}
		self.GiveResources(newResources)
		
		return self.GetResources()
