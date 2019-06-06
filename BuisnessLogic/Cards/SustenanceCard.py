from typing import Dict
from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum
from Core.resourceContainer import ActiveResourceContainer
from Common.Entities.multicombination import Combination
from BuisnessLogic.Actions import *

class SustenanceCard(BaseCard, ActiveResourceContainer):
	
	def __init__(self):
		self._name = "Sustenance"
		self._id = 19
		self._level = -1
		self._actions = Combination(
			ActionCombinationEnum.AndThen,
			takeAccumulatedItemsAction.TakeAccumulatedItemsAction(),
			placeATileAction.PlaceATileAction( TileTypeEnum.meadowFieldTwinTile) )
		
	def RefillAction(self) -> Dict[ResourceTypeEnum, int]:
		if self.HasResources():
			self.GiveResource( ResourceTypeEnum.vegetable, 1 )
		self.GiveResource( ResourceTypeEnum.grain, 1 )
		
		return self.GetResources()
