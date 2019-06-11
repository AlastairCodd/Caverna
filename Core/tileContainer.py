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
		self._height = height
		self._width = width
		
		self._tileCount = height * width
		
		self._tiles: List[BaseTile]
		
		self._twinTiles = [
			TileTypeEnum.meadowFieldTwin,
			TileTypeEnum.cavernTunnelTwin,
			TileTypeEnum.cavernCavernTwin,
			TileTypeEnum.pastureTwin,
			TileTypeEnum.oreMineDeepTunnelTwin ]
		self._outdoorTiles = [
			Tile
		
	def GetTiles(self) -> List[BaseTile]:
		return self._tiles
		
	def GetEffects(self) -> List[BaseEffect]:
		effects = map(lambda tile: tile.GetEffects(), self._tiles)
		return list(effects)
		
	def GetEffectsOfType(self, type) -> List[BaseEffect]:
		result = [x for x in self.GetEffects() if isinstance(x, type)]
		return result
		
	def PlaceTile(self, tile: BaseTile, location: int, direction: TileDirectionEnum = None) -> bool:
		if tile is None:
			raise ValueError("base tile")
			
		if location < 0 or location > 47:
			raise ValueError("base tile")
		
		if tile in self._twinTiles and direction is None:
			raise ValueError("direct cannot be null if tile is a twin tile")
			
		availableLocations = self.GetAvailableLocations( tile )
		if location in availableLocations:
			self._tiles.append( tile )
		
	def GetAvailableLocations(self, tile: BaseTile) -> List[int]:
		if tile is None:
			raise ValueError
		if 
		
	def GetAdjacentTiles(self, location: int) -> List[int]:
		if location < 0 or location > self._tileCount:
			raise ValueError
	
		directionOffset = {
			TileDirectionEnum.up: -8,
			TileDirectionEnum.down: 8,
			TileDirectionEnum.left: -1,
			TileDirectionEnum.right: 1 }
		
		adjacentDirectionCondition = {
			TileDirectionEnum.up: lambda adjloc: adjloc > 0,
			TileDirectionEnum.down: lambda adjloc: adjloc < self._tileCount,
			TileDirectionEnum.left: lambda adjloc: adjloc % self._width != 7,
			TileDirectionEnum.right: lambda adjloc: adjloc % self._width != 0 }
		
		result = []
		
		for x in directionOffset:
			adjacentLocation = location + directionOffset[x]
			if adjacentDirectionCondition[x]( adjacentLocation ):
				result.append( adjacentLocation )
				
		return result