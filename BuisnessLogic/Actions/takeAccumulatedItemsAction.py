from Core.baseAction import BaseAction
from Core.baseCard import BaseCard
from player import Player

class TakeAccumulatedItemsAction(BaseAction):
	def Invoke(
		self,
		player: Player,
		activeCard: BaseCard ) -> bool:
		if player is None:
			raise ValueException("player")
		
		player.GiveResources( activeCard.GetResources() )
		activeCard.ClearResources()
		