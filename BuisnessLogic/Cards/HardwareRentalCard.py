from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum
from Common.Entities.multicombination import Combination
from BuisnessLogic.Actions import *

class HardwareRentalCard(BaseCard):
	
	def __init__(self):
		self._name = "Hardware Rental"
		self._id = 9
		self._level = -1
		self._actions = Combination(
			ActionCombinationEnum.AndThenOr,
			receiveAction.ReceiveAction( {ResourceTypeEnum.wood, 2} ),
			Combination(
				ActionCombinationEnum.AndThenOr,
				goOnAnExpeditionAction.GoOnAnExpeditionAction( 2 ),
				sowAction.SowAction() ) )
