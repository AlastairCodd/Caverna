from typing import Dict
from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum
from Core.resourceContainer import ResourceContainer
from Common.Entities.multicombination import Combination
from BuisnessLogic.Actions import *

class LoggingCard(BaseCard, ResourceContainer):
	
	def __init__(self):
		self._name = "Logging"
		self._id = 13
		self._level = -1
		self._actions = Combination(
			ActionCombinationEnum.AndThenOr,
			takeAccumulatedItemsAction.TakeAccumulatedItemsAction(),
			goOnAnExpeditionAction.GoOnAnExpeditionAction( 1 ) )
		
	def RefillAction(self) -> Dict[ResourceTypeEnum, int]:
		self.GiveResource( ResourceTypeEnum.wood, 3 )
		
		return self.GetResources()
