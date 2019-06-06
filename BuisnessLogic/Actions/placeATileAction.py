from player import Player
from Core.baseAction import BaseAction
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from Core.baseCard import BaseCard

class PlaceATileAction(BaseAction):
	_tileType: TileTypeEnum
	
	def __init__(self, tileType: TileTypeEnum):
		self._tileType = tileType
	
	def Invoke(
		self,
		player: Player,
		activeCard: BaseCard ) -> bool:
		if player is None:
			raise ValueException("player")
		
		raise NotImplementedError()