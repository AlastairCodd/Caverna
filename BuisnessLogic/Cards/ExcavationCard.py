from typing import Dict
from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from Common.Entities.multiconditional import Conditional
from BuisnessLogic.Actions.takeAccumulatedItemsAction import TakeAccumulatedItemsAction
from BuisnessLogic.Actions.placeATileAction import PlaceATileAction

class ExcavationCard(BaseCard):
	
	def __init__(self):
		self._name = "Drift Mining"
		self._id = 4
		self._level = -1
		self._actions = Conditional( 
			ActionCombinationEnum.AndThen,
			TakeAccumulatedItemsAction(),
			Conditional( 
				ActionCombinationEnum.Or,
				PlaceATileAction( TileTypeEnum.cavernTunnelTwin ),
				PlaceATileAction( TileTypeEnum.cavernCavernTwin ) ) )
		
	def RefillAction(self) -> Dict[ResourceTypeEnum, int]:
		newResources = {ResourceTypeEnum.stone: 1} if self.HasResources() else {ResourceTypeEnum.stone: 2}
		self.GiveResources(newResources)
		
		return self.GetResources()
