from typing import Dict
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum

class BaseAction(object):
	
	def Invoke(
		self,
		player,
		accumulatedItems: Dict[ResourceTypeEnum, int] ) -> bool:
		raise NotImplementedError("abstract base action class")