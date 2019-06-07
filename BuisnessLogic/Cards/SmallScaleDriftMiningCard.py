from typing import Dict
from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from Core.resourceContainer import ActiveResourceContainer
from Common.Entities.multicombination import Combination
from BuisnessLogic.Actions import *

class SmallScaleDriftMiningCard(BaseCard):
	
	def __init__(self):
		self._name = "Small Scale Drift Mining"
		self._id = 13
		self._level = -1
		self._actions = Combination(
			ActionCombinationEnum.AndOr,
			receiveAction.ReceiveAction( {ResourceTypeEnum.stone:1} ),
			placeATileAction.PlaceATileAction( TileTypeEnum.cavern ) )
