from typing import Dict
from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from Common.Entities.multiconditional import Conditional
from BuisnessLogic.Actions.takeAccumulatedItemsAction import TakeAccumulatedItemsAction
from BuisnessLogic.Actions.placeATileAction import PlaceATileAction

class DriftMiningCard(BaseCard):
	
	def __init__(self):
		self._name = "Drift Mining"
		self._id = 2
		self._level = -1
		self._actions = Conditional( 
			ActionCombinationEnum.AndThen,
			TakeAccumulatedItemsAction(),
			PlaceATileAction( TileTypeEnum.cavernTunnelTwin ) )
		
	def RefillAction(self) -> Dict[ResourceTypeEnum, int]:
		self.GiveResource( ResourceTypeEnum.stone, 2 )
		
		return self.GetResources()
