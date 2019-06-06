from typing import Dict
from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from Core.resourceContainer import ResourceContainer
from Common.Entities.multicombination import Combination
from BuisnessLogic.Actions import *

class FenceBuildingCard(BaseCard, ResourceContainer):
	
	def __init__(self):
		self._name = "Fence Building"
		self._id = 5
		self._level = -1
		self._actions = Combination(
			ActionCombinationEnum.AndThen,
			takeAccumulatedItemsAction.TakeAccumulatedItemsAction(),
			Combination(
				ActionCombinationEnum.AndOr,
				Combination(
					ActionCombinationEnum.AndThen,
					payAction.PayAction( {ResourceTypeEnum.wood, 2} ),
					placeATileAction.PlaceATileAction( TileTypeEnum.pastureTwin ) ),
				Combination(
					ActionCombinationEnum.AndThen,
					payAction.PayAction( {ResourceTypeEnum.wood, 4} ),
					placeATileAction.PlaceATileAction( TileTypeEnum.pastureTwin )
				) ) )
		
	def RefillAction(self) -> Dict[ResourceTypeEnum, int]:
		newResources = {ResourceTypeEnum.wood: 1} if self.HasResources() else {ResourceTypeEnum.wood: 2}
		self.GiveResources(newResources)
		
		return self.GetResources()
