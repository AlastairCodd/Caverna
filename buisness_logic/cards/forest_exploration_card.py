from typing import Dict
from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum
from Core.resourceContainer import ResourceContainer
from Common.Entities.multicombination import Combination
from BuisnessLogic.Actions import *

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
