from typing import Dict, Iterable
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum
from Core.baseAction import BaseAction
from Common.Entities.dwarf import Dwarf

class BaseCard(object):
	_name: str = "Uninitialised"
	_id: int = -1
	_level: int = -1
	_actions: Iterable[BaseAction] = []
	_actionCombinationType: ActionCombinationEnum = ActionCombinationEnum.EitherOr
	_currentItems: Dict[ResourceTypeEnum, int] = {}
	
	def RefillAction(self) -> Dict[ResourceTypeEnum, int]:
		raise NotImplementedError("abstract base card class")
		
	def ActivateCard(
			self, 
			player,
			dwarf: Dwarf ) -> bool:
		return False