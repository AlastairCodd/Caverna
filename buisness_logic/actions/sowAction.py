from player import Player
from Core.baseAction import BaseAction
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from Core.baseCard import BaseCard

class SowAction(BaseAction):

	def Invoke(
		self,
		player: Player,
		activeCard: BaseCard ) -> bool:
		if player is None:
			raise ValueException("player")
		
		raise NotImplementedError()