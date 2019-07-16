from typing import Dict
from core.baseClasses.base_card import BaseCard
from core.enums.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from common.entities.multicombination import Combination
from buisness_logic.actions import *

class GrowthCard(BaseCard):
	
	def __init__(self):
		self._name = "Growth"
		self._id = 7
		self._level = -1
		self._actions = Combination( 
			ActionCombinationEnum.AndThen,
			receiveAction.ReceiveAction( {
				ResourceTypeEnum.wood: 1,
				ResourceTypeEnum.stone: 1,
				ResourceTypeEnum.ore: 1,
				ResourceTypeEnum.food: 1,
				ResourceTypeEnum.coin: 2 } ),
			getABabyDwarfAction.GetABabyDwarfAction() )