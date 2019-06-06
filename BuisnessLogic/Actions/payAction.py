from typing import Dict
from player import Player
from Core.baseAction import BaseAction
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from Core.baseCard import BaseCard

class PayAction(BaseAction):
	_payItems = Dict[ResourceTypeEnum, int]
		
	def __init__(self, payItems: Dict[ResourceTypeEnum, int]):
		if payItems is None:
			raise ValueException("payItems")
		self._payItems = payItems
	
	def Invoke(
		self,
		player: Player,
		activeCard: BaseCard ) -> bool:
		if player is None:
			raise ValueException("player")
		
		raise NotImplementedError()