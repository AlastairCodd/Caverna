from player import Player
from Core.baseEffect import BaseEffect

class BaseBoardEffect(BaseEffect):
	def Invoke(self, player: Player) -> bool:
		raise NotImplementedException("base population effect class")
	
class FurnishTunnelsEffect(BaseBoardEffect):
	def Invoke(self, player: Player) -> bool:
		raise NotImplementedException()
		
class TwinTilesOverhangEffect(BaseBoardEffect):
	def Invoke(self, player: Player) -> bool:
		raise NotImplementedException()