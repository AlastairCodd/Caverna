from typing import Dict
from Core.cavernaEnums import TileTypeEnum
from Common.Entities.tileEntity import TileEntity

class TileContainerDefault(object):

    def assign(
        self, 
        currentTiles: Dict[int, TileEntity]) -> Dict[int, TileEntity]:
        '''Fills the given dictionary with the default tile layout'''
        if currentTiles is None: raise ValueError("currentTiles")
        for id in range(48):
            if currentTiles[id] is None:
                currentTiles[id] = tileEntity.TileEntity( id )
                
            if (id < 8 or id > 40 or id % 8 == 0 or id % 8 == 7):
                currentTiles[id]._tileType = TileTypeEnum.unavailable
            elif id % 8 < 4:
                currentTiles[id]._tileType = TileTypeEnum.forest
            else:
                currentTiles[id]._tileType = TileTypeEnum.underground

        currentTiles = self._specificIntialTileOverrides( currentTiles )
        return currentTiles
        
    def _specificIntialTileOverrides(
        self, 
        currentTiles: Dict[int, TileEntity]) -> Dict[int, TileEntity]:
        '''Overrides specific current tiles
        
        currentTiles: a dictionary of int to TileTypeEnum. This cannot be null
        returns: currentTiles'''
        if currentTiles is None: raise ValueError("currentTiles")
        currentTiles[28]._tileType = TileTypeEnum.cavern
        currentTiles[36]._tileType = TileTypeEnum.furnishedDwelling
        
        return currentTiles
