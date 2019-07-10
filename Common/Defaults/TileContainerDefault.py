from typing import Dict
from Core.cavernaEnums import TileTypeEnum

class TileContainerDefault(object):

	def assign(
		self, 
		currentTiles: Dict[int, TileTypeEnum]) -> Dict[int, TileTypeEnum]:
		'''Fills the given dictionary with the default tile layout'''
		if currentTiles is None: raise ValueError("currentTiles")
		for x in range(48):
            if currentTiles[x] is None:
                currentTiles[x] = tileEntity.TileEntity( x )
                
			if (x < 8 or x > 40 or x % 8 == 0 or x % 8 == 7):
				currentTiles[x]._tileType = TileTypeEnum.unavailable
			elif x % 8 < 4:
				currentTiles[x]._tileType = TileTypeEnum.forest
			else:
				currentTiles[x]._tileType = TileTypeEnum.underground

		currentTiles = self._specificIntialTileOverrides( currentTiles )
		return currentTiles
		
	def _specificIntialTileOverrides(
		self, 
		currentTiles: Dict[int, TileTypeEnum]) -> Dict[int, TileTypeEnum]:
		'''Overrides specific current tiles
		
		currentTiles: a dictionary of int to TileTypeEnum. This cannot be null
		returns: currentTiles'''
		if currentTiles is None: raise ValueError("currentTiles")
        currentTiles[28]._tileType = TileTypeEnum.cavern
        currentTiles[36]._tileType = TileTypeEnum.furnishedDwelling
        
		return currentTiles
