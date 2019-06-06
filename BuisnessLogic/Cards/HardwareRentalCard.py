from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum
from player import Player
from dwarf import Dwarf
#from action import Action

class HardwareRentalCard(BaseCard):
	
	def __init__(self):
		self._name = "Hardware Rental"
		self._id = 9
		self._level = -1
		self._actionCombinationType = ActionCombinationEnum.AndThenOr
		self._actions = [
			Receive( ResourceTypeEnum.wood, 2 ),
			GoOnAnExpedition(),
			Sow()
		]
