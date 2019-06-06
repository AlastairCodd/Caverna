from typing import Dict
from Core.cavernaEnums import ResourceTypeEnum
from Core.baseCard import BaseCard
from Core.baseAction import BaseAction
from player import Player

class ReceiveAction(BaseAction):
	_receiveItems = Dict[ResourceTypeEnum, int]
	
	def __init__(self, receiveItems: Dict[ResourceTypeEnum, int]):
		if receiveItems is None:
			raise ValueException("receiveItems")
		self._receiveItems = receiveItems
	
	def Invoke(
		self,
		player: Player,
		activeCard: BaseCard ) -> bool:
		if player is None:
			raise ValueException("player")
		
		player.GiveResources( self._receiveItems )
		