from typing import Dict
from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum
from Core.resourceContainer import ResourceContainer
from Common.Entities.multicombination import Combination
from BuisnessLogic.Actions import *

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
		
	def RefillAction(self) -> Dict[ResourceTypeEnum, int]:
		self.GiveResource( ResourceTypeEnum.food, 1 )
		
		return self.GetResources()
