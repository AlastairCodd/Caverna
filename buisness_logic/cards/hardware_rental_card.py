from core.baseClasses.base_card import BaseCard
from core.enums.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum
from common.entities.multicombination import Combination
from buisness_logic.actions import *

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
