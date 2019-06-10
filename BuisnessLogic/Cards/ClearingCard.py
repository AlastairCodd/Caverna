from typing import Dict
from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from Core.resourceContainer import ActiveResourceContainer
from Common.Entities.multicombination import Combination
from BuisnessLogic.Actions import *

class ClearingCard(BaseCard, ActiveResourceContainer):
	
	def __init__(self):
		self._name = "Clearing"
		self._id = 0
		self._level = -1
		self._actions = Combination( 
			ActionCombinationEnum.AndThenOr,
			takeAccumulatedItemsAction.TakeAccumulatedItemsAction(),
			placeATileAction.PlaceATileAction( TileTypeEnum.meadowFieldTwin ) )
		super(ClearingCard, self).__init__()
		
	def RefillAction(self) -> Dict[ResourceTypeEnum, int]:
		self.GiveResource( ResourceTypeEnum.wood, 2 )
		
		return self.GetResources()
