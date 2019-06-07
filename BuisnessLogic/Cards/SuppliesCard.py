from typing import Dict
from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum
from Core.resourceContainer import ActiveResourceContainer
from Common.Entities.multicombination import Combination
from BuisnessLogic.Actions import *

class SuppliesCard(BaseCard):
	
	def __init__(self):
		self._name = "Supplies"
		self._id = 18
		self._level = -1
		self._actions = receiveAction.ReceiveAction( {
			ResourceTypeEnum.wood:1,
			ResourceTypeEnum.stone:1,
			ResourceTypeEnum.ore:1,
			ResourceTypeEnum.food:1,
			ResourceTypeEnum.coin:2 } )
