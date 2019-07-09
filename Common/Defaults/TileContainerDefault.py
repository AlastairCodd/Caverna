from typing import Dict
from Core.cavernaEnums import TileTypeEnum

class TileContainerDefault(object):

	def assign(
		self, 
		currentTiles: Dict[int, TileTypeEnum]) -> Dict[int, TileTypeEnum]:
		'''Fills the given dictionary with the default tile layout'''
		if currentTiles is None: raise ValueError("currentTiles")
		for x in range(48):
			if (x < 8 or x > 40 or x % 8 == 0 or x % 8 == 7):
				currentTiles[x] = TileTypeEnum.unavailable
			elif x % 8 < 4:
				currentTiles[x] = TileTypeEnum.forest
			else:
				currentTiles[x] = TileTypeEnum.underground

		currentTiles = self._specificIntialTileOverrides( currentTiles )
		return currentTiles
		
	def _specificIntialTileOverrides(
		self, 
		currentTiles: Dict[int, TileTypeEnum]) -> Dict[int, TileTypeEnum]:
		'''Overrides specific current tiles
		
		currentTiles: a dictionary of int to TileTypeEnum. This cannot be null
		returns: currentTiles'''
		if currentTiles is None: raise ValueError("currentTiles")
		currentTiles.update(
			{
				28: TileTypeEnum.cavern,
				36: TileTypeEnum.furnishedDwelling } )
		return currentTiles
