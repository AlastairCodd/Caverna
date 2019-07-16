from typing import Dict
from core.baseClasses.base_card import BaseCard
from core.enums.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum
from common.entities.multicombination import Combination
from buisness_logic.actions import *

class Imitation1Card(BaseCard):
	
	def __init__(self):
		self._name = "Imitation"
		self._id = 10
		self._level = -1
		self._actions = Combination(
			ActionCombinationEnum.AndThen,
			payAction.PayAction( {ResourceTypeEnum.food, 1} ),
			useAnotherCardAction.UseAnotherCardAction() )