from typing import Dict
from core.baseClasses.base_card import BaseCard
from core.enums.cavernaEnums import ResourceTypeEnum
from core.containers.resource_container import ResourceContainer
from buisness_logic.actions import *

class DepotCard(BaseCard, ResourceContainer):
	
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
