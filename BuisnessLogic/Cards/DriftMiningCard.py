from typing import Dict
from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from Core.resourceContainer import ActiveResourceContainer
from Common.Entities.multicombination import Combination
from BuisnessLogic.Actions import *

class DriftMiningCard(BaseCard, ActiveResourceContainer):
	
	def __init__(self):
		self._name = "Drift Mining"
		self._id = 2
		self._level = -1
		self._actions = Combination( 
			ActionCombinationEnum.AndThen,
			takeAccumulatedItemsAction.TakeAccumulatedItemsAction(),
			placeATileAction.PlaceATileAction( TileTypeEnum.cavernTunnelTwin ) )
		
	def RefillAction(self) -> Dict[ResourceTypeEnum, int]:
		self.GiveResource( ResourceTypeEnum.stone, 2 )
		
		return self.GetResources()
