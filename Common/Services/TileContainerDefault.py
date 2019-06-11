from typing import Dict
from Core.cavernaEnums import TileTypeEnum

class TileContainerDefault(object):

	def AssignInitialTiles(self, currentTiles: Dict[int, TileTypeEnum]) -> Dict[int, TileTypeEnum]:
		for x in range(48):
			if (x < 8 or x > 40 or x % 8 == 0 or x % 8 == 7):
				currentTiles[x] = TileTypeEnum.unavailable
			elif x % 8 < 4:
				currentTiles[x] = TileTypeEnum.forest
			else:
				currentTiles[x] = TileTypeEnum.underground

		currentTiles = self._specificIntialTileOverrides( currentTiles )
		return currentTiles
		
	def _specificIntialTileOverrides(self, currentTiles: Dict[int, TileTypeEnum]) -> Dict[int, TileTypeEnum]:
		currentTiles[36] = TileTypeEnum.furnishedDwelling
		currentTiles[28] = TileTypeEnum.cavern
		return currentTiles
