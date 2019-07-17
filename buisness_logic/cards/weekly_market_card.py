from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum
from Common.Entities.multicombination import Combination
from BuisnessLogic.Actions import *

class WeeklyMarketCard(BaseCard):
	
	def __init__(self):
		self._name = "Weekly Market"
		self._id = 20
		self._level = -1
		self._actions = Combination(
			ActionCombinationEnum.AndThenOr,
			receiveAction.ReceiveAction( {ResourceTypeEnum.coin, 4} ),
			buyFromMarketAction.BuyFromMarketAction() )