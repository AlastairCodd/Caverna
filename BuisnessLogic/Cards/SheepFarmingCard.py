from typing import Dict
from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from Core.resourceContainer import ResourceContainer
from Common.Entities.multicombination import Combination
from BuisnessLogic.Actions import *

class SheepFarmingCard(BaseCard, ResourceContainer):
	
	def __init__(self):
		self._name = "Sheep Farming"
		self._id = 23
		self._level = 1
		self._actions = Combination(
			ActionCombinationEnum.AndThen,
			Combination(
				ActionCombinationEnum.AndOr,
				Combination(
					ActionCombinationEnum.AndOr,
					Combination(
						ActionCombinationEnum.AndThen,
						payAction.PayAction( {ResourceTypeEnum.wood, 2} ),
						placeATileAction.PlaceATileAction( TileTypeEnum.pasture ) ),
					Combination(
						ActionCombinationEnum.AndThen,
						payAction.PayAction( {ResourceTypeEnum.wood, 4} ),
						placeATileAction.PlaceATileAction( TileTypeEnum.pastureTwin ) ) ),
				Combination(
					ActionCombinationEnum.AndThen,
					payAction.PayAction( {ResourceTypeEnum.stone, 1} ),
					placeATileAction.PlaceAStableAction() ) ),
			takeAccumulatedItemsAction.TakeAccumulatedItemsAction() )
		
	def RefillAction(self) -> Dict[ResourceTypeEnum, int]:
		self.GiveResource( ResourceTypeEnum.sheep, 1 )
		
		return self.GetResources()
