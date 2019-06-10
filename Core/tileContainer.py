from typing import List

class TileContainer(object):
	
	def __init__(self, height=):
		self._tiles: List[BaseTile] = []
		self._twinTiles = [
			meadowFieldTwin,
			cavernTunnelTwin,
			cavernCavernTwin,
			pastureTwin,
			oreMineDeepTunnelTwin ]
		
	def GetTiles(self) -> List[BaseTile]:
		return self._tiles
		
	def GetEffects(self) -> List[baseEffect]:
		effects = map(lambda tile: tile.GetEffects, self._tiles)
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
		directionOffset = 