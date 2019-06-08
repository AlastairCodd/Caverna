from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum
from Core.resourceContainer import ResourceContainer
from Common.Entities.multicombination import Combination
from BuisnessLogic.Actions import *

class AdventureCard(BaseCard):
	
	def __init__(self):
		self._name = "Adventure"
		self._id = 31
		self._level = 4
		
		self._actions = Combination(
			ActionCombinationEnum.AndThenOr,
			giveDwarf
			Conditional(
				ActionCombinationEnum.AndOr,
				Conditional(
					ActionCombinationEnum.AndThen,
					payAction.PayAction( {ResourceTypeEnum.ore: 2} ),
					receiveAction.ReceiveAction( {ResourceTypeEnum.coins: 2, ResourceTypeEnum.food: 1} ) ),
				Conditional(
					ActionCombinationEnum.AndThen,
					payAction.PayAction( {ResourceTypeEnum.ore: 2} ),
					receiveAction.ReceiveAction( {ResourceTypeEnum.coins: 2, ResourceTypeEnum.food: 1} ) ) ) )