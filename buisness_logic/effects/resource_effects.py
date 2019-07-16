from common.entities.player import Player
from core.baseClasses.base_effect import BaseEffect

class BaseResourceEffect(BaseEffect):
	def invoke(self, player: Player) -> bool:
		raise NotImplementedException("base resource effect class")
	
class ReceiveConditional(BaseResourceEffect):
	def __init__(self, increaseBy: int):
		self._increaseBy = increaseBy

	def invoke(self, player: Player) -> bool:
		raise NotImplementedException()
		
class AllowSixthDwarfEffect(BasePopulationEffect):
	def invoke(self, player: Player) -> bool:
		raise NotImplementedException()
		
class ReceiveOnPurchasedEffect(BaseResourceEffect):
	def __init__(self):
		pass