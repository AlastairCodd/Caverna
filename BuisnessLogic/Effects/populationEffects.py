from player import Player
from Core.baseEffect import BaseEffect

class BasePopulationEffect(BaseEffect):
	def Invoke(self, player: Player) -> bool:
		raise NotImplementedException("base population effect class")
	
class IncreasePopulationCapEffect(BasePopulationEffect):
	def __init__(self, increaseBy: int):
		self._increaseBy = increaseBy

	def Invoke(self, player: Player) -> bool:
		raise NotImplementedException()
		
class AllowSixthDwarfEffect(BasePopulationEffect):
	def Invoke(self, player: Player) -> bool:
		raise NotImplementedException()