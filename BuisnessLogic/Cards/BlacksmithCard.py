from typing import Dict
from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum
from Core.resourceContainer import ActiveResourceContainer
from Common.Entities.multicombination import Combination
from BuisnessLogic.Actions import *

class BlacksmithCard(BaseCard):
	
	def __init__(self):
		self._name = "Blacksmith"
		self._id = 21
		self._level = 1
		self._actions = Combination(
			ActionCombinationEnum.AndThenOr,
			giveDwarfAWeaponAction.GiveDwarfAWeaponAction(),
			goOnAnExpeditionAction.GoOnAnExpeditionAction( 3 ) )
