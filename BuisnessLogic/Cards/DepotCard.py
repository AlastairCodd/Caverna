from typing import Dict
from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum
from Core.resourceContainer import ActiveResourceContainer
from BuisnessLogic.Actions import *

class DepotCard(BaseCard, ActiveResourceContainer):
	
	def __init__(self):
		self._name = "Depot"
		self._id = 1
		self._level = -1
		self._actions = takeAccumulatedItemsAction.TakeAccumulatedItemsAction()
		
	def RefillAction(self) -> Dict[ResourceTypeEnum, int]:
		newResources = {
			ResourceTypeEnum.wood: 2, 
			ResourceTypeEnum.ore: 2 }
		self.GiveResources(newResources)
		
		return self.GetResources()
