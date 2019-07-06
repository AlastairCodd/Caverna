from player import Player
from Core.baseAction import BaseAction
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from Core.baseCard import BaseCard

class PlaceATileAction(BaseAction):
	def __init__(self, tileType: TileTypeEnum):
		self._tileType = tileType
	
	def Invoke(
		self,
		player: Player,
		activeCard: BaseCard ) -> bool:
		'''An action where a player:
			- chooses a tile
			- pays the cost (taking additional discount effects into account)
			- places the tile on the board in an available location'''
		if player is None: raise ValueException("player")
		
		
		
		position = player.get_player_input(self)
		
class PlaceAStableAction(BaseAction):
	
	def Invoke(
		self,
		player: Player,
		activeCard: BaseCard ) -> bool:
		if player is None:
			raise ValueException("player")
		
		raise NotImplementedError()
