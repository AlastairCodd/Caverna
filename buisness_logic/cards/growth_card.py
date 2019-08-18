from typing import Dict
from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from Core.resourceContainer import ResourceContainer
from Common.Entities.multicombination import Combination
from BuisnessLogic.Actions import *

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