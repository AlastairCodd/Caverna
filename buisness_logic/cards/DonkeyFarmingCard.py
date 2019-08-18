from typing import Dict
from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from Core.resourceContainer import ActiveResourceContainer
from Common.Entities.multicombination import Combination
from BuisnessLogic.Actions import *

class DonkeyFarmingCard(BaseCard, ActiveResourceContainer):
	
	def __init__(self):
		self._name = "Donkey Farming"
		self._id = 24
		self._level = 2
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
		super().__init__()

	def RefillAction(self) -> Dict[ResourceTypeEnum, int]:
		self.GiveResource( ResourceTypeEnum.donkey, 1 )
		
		return self.GetResources()
