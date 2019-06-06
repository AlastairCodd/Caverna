from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from Core.resourceContainer import ActiveResourceContainer
from Common.Entities.multicombination import Combination
from BuisnessLogic.Actions import *

class OreDeliveryCard(BaseCard, ActiveResouceContainer):
	
	def __init__(self):
		self._name = "Ore Delivery"
		self._id = 30
		self._level = 3
		self._actions = Combination(
			ActionCombinationEnum.AndThen,
			takeAccumulatedItemsAction.TakeAccumulatedItemsAction() )
			
	def RefillAction(self) -> Dict[ResourceTypeEnum, int]:
		self.GiveResource( 
			ResourceTypeEnum.stone: 1,
			ResourceTypeEnum.ore: 1 )
		
		return self.GetResources()
