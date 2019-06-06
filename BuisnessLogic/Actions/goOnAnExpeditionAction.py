from Core.baseAction import BaseAction
from Core.baseCard import BaseCard
from player import Player

class GoOnAnExpeditionAction(BaseAction):
	_level: int

	def __init__(self, level: int):
		if level < 1 or level > 4:
			raise ValueException("level")
		self._level = level

	def Invoke(
		self,
		player: Player,
		activeCard: BaseCard ) -> bool:
		if player is None:
			raise ValueException("player")
		raise NotImplementedException
		