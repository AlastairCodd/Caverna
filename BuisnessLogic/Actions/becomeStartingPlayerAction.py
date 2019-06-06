from typing import Dict
from Core.cavernaEnums import ResourceTypeEnum
from Core.baseCard import BaseCard
from Core.baseAction import BaseAction
from player import Player

class BecomeStartingPlayerAction(BaseAction):
	def Invoke(
		self,
		player: Player,
		activeCard: BaseCard ) -> bool:
		if player is None:
			raise ValueException("player")
		
		raise NotImplementedError()
		