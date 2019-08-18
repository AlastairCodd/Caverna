from typing import Dict
from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from Core.resourceContainer import ActiveResourceContainer
from Common.Entities.multicombination import Combination
from BuisnessLogic.Actions import *

class OreDeliveryCard(BaseCard, ActiveResourceContainer):
	
	def __init__(self):
		self._name = "Ore Delivery"
		self._id = 30
		self._level = 3
		self._actions = takeAccumulatedItemsAction.TakeAccumulatedItemsAction()
		super(OreDeliveryCard, self).__init__()
		
	def RefillAction(self) -> Dict[ResourceTypeEnum, int]:
		self.GiveResources( { 
			ResourceTypeEnum.stone: 1,
			ResourceTypeEnum.ore: 1 } )
		
		return self.GetResources()
