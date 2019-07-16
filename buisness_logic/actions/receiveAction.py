from typing import Dict
from core.enums.cavernaEnums import ResourceTypeEnum
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_action import BaseAction
from common.entities.player import Player

class ReceiveAction(BaseAction):
	_receiveItems: Dict[ResourceTypeEnum, int]
	
	def __init__(self, receiveItems: Dict[ResourceTypeEnum, int]):
		if receiveItems is None:
			raise ValueError("receiveItems")
		self._receiveItems = receiveItems
	
	def Invoke(
		self,
		player: Player,
		activeCard: BaseCard ) -> bool:
		if player is None:
			raise ValueError("player")
		
		player.GiveResources( self._receiveItems )
		