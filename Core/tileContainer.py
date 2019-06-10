from typing import List
from Core.cavernaEnums import TileDirectionEnum, TileTypeEnum
from Core.baseEffect import BaseEffect
from Core.baseTile import BaseTile

class TileContainer(object):
	
	def __init__(self, height=6, width=8):
		if height < 0:
			raise ValueError("height must be greater than 0")
		if width < 0:
			raise ValueError("width must be greater than 0")
		self._tiles: List[BaseTile] = [x for x in range(height*width)]
		self._twinTiles = [
			TileTypeEnum.meadowFieldTwin,
			TileTypeEnum.cavernTunnelTwin,
			TileTypeEnum.cavernCavernTwin,
			TileTypeEnum.pastureTwin,
			TileTypeEnum.oreMineDeepTunnelTwin ]
		
	def GetTiles(self) -> List[BaseTile]:
		return self._tiles
		
	def GetEffects(self) -> List[BaseEffect]:
		effects = map(lambda tile: tile.GetEffects(), self._tiles)
		return list(effects)
		
	def GetEffectsOfType(self, type) -> List[baseEffect]:
		result = [x for x in self.GetEffects() if isinstance(x, type)]
		return result
		
	def PlaceTile(self, tile: BaseTile, location: int, direction: TileDirectionEnum = None) -> bool:
		if tile is None:
			raise ValueError("base tile")
			
		if location < 0 or location > 47:
			raise ValueError("base tile")
		
		if tile in self._twinTiles and direction is None:
			raise ValueError("direct cannot be null if tile is a twin tile")
		
	def GetAdjacentTile(self, location: int, direction: TileDirectionEnum) -> int:
		directionOffset = {
			TileDirectionEnum.up: -8,
			TileDirectionEnum.down: 8,
			TileDirectionEnum.left: -1,
			TileDirectionEnum.right: 1 }
		raise NotImplementedException()