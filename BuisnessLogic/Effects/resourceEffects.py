from player import Player
from Core.baseEffect import BaseEffect

class BaseResourceEffect(BaseEffect):
	def Invoke(self, player: Player) -> bool:
		raise NotImplementedException("base resource effect class")
	
class ReceiveConditional(BaseResourceEffect):
	def __init__(self, increaseBy: int):
		self._increaseBy = increaseBy

	def Invoke(self, player: Player) -> bool:
		raise NotImplementedException()
		
class AllowSixthDwarfEffect(BasePopulationEffect):
	def Invoke(self, player: Player) -> bool:
		raise NotImplementedException()
		
class ReceiveOnPurchasedEffect(BaseResourceEffect):
	def __init__(self):
		