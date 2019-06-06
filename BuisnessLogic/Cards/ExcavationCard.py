from typing import Dict
from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from Core.resourceContainer import ResourceContainer
from Common.Entities.multicombination import Combination
from BuisnessLogic.Actions import *

class ExcavationCard(BaseCard, ResourceContainer):
	
	def __init__(self):
		self._name = "Excavation"
		self._id = 4
		self._level = -1
		self._actions = Combination( 
			ActionCombinationEnum.AndThen,
			takeAccumulatedItemsAction.TakeAccumulatedItemsAction(),
			Combination( 
				ActionCombinationEnum.Or,
				placeATileAction.PlaceATileAction( TileTypeEnum.cavernTunnelTwin ),
				placeATileAction.PlaceATileAction( TileTypeEnum.cavernCavernTwin ) ) )
		
	def RefillAction(self) -> Dict[ResourceTypeEnum, int]:
		newResources = {ResourceTypeEnum.stone: 1} if self.HasResources() else {ResourceTypeEnum.stone: 2}
		self.GiveResources(newResources)
		
		return self.GetResources()
