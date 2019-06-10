from typing import Dict
from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from Core.resourceContainer import ActiveResourceContainer
from Common.Entities.multicombination import Combination
from BuisnessLogic.Actions import *

class DriftMining2Card(BaseCard, ActiveResourceContainer):
	
	def __init__(self):
		self._name = "Drift Mining 2"
		self._id = 3
		self._level = -1
		self._actions = Combination( 
			ActionCombinationEnum.AndThen,
			takeAccumulatedItemsAction.TakeAccumulatedItemsAction(),
			placeATileAction.PlaceATileAction( TileTypeEnum.cavernTunnelTwin ) )
		super(DriftMining2Card, self).__init__()
	
	def RefillAction(self) -> Dict[ResourceTypeEnum, int]:
		self.GiveResource( ResourceTypeEnum.stone, 1 )
		
		return self.GetResources()
