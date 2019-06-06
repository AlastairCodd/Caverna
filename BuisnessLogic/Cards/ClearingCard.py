from typing import Dict
from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from player import Player
from Common.Entities.dwarf import Dwarf
import BuisnessLogic.Actions

class ClearingCard(BaseCard):
	
	def __init__(self):
		self._name = "Clearing"
		self._id = 0
		self._level = -1
		self._actionCombinationType = ActionCombinationEnum.AndThen
		self._actions = [
			TakeAccumulatedItemsAction(),
			PlaceATileAction( TileTypeEnum.meadowFieldTwin ) 
		]
		self._currentItems = { ResourceTypeEnum.wood: 0 }
		
	def RefillAction(self) -> Dict[ResourceTypeEnum, int]:
		self._currentItems.setdefault( ResourceTypeEnum.wood, 0 )
		self._currentItems[ ResourceTypeEnum.wood ] += 2
		return self._currentItems