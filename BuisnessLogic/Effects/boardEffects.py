from typing import Dict, List
from player import Player
from Core.baseEffect import BaseEffect
from Core.cavernaEnums import TileTypeEnum
from Common.Services.TileTwinDefault import TileTwinDefault

class BaseBoardEffect(BaseEffect):
	def Invoke(self, source: Dict[TileTypeEnum, List[TileTypeEnum]]) -> Dict[TileTypeEnum, List[TileTypeEnum]]:
		raise NotImplementedException("base board effect class")

class ChangeRequisiteEffect(BaseBoardEffect):
	def __init__(self, tiles: List[TileTypeEnum], newRequisites: List[TileTypeEnum]):
		if tiles is None:
			raise ValueError()
		if newRequisites is None:
			raise ValueError()
			
		self._tiles: List[TileTypeEnum] = tiles
		self._newRequisites: List[TileTypeEnum] = newRequisites
	
	def Invoke(self, source: Dict[TileTypeEnum, List[TileTypeEnum]]) -> Dict[TileTypeEnum, List[TileTypeEnum]]:
		if source is None:
			raise ValueError()
		
		for tile in self._tiles:
			source[tile].extend(self._newRequisites)
		return source

class FurnishTunnelsEffect(ChangeRequisiteEffect):
	def __init__(self):
		super().__init__(
			[TileTypeEnum.furnishedCavern, TileTypeEnum.furnishedDwelling], 
			[TileTypeEnum.tunnel, TileTypeEnum.deepTunnel] )
		
class TwinTilesOverhangEffect(ChangeRequisiteEffect):
	def __init__(self):
		twinDefault = TileTwinDefault.TileTwinDefault()
		twinTiles = twinDefault.Assign( [] )
		super().__init__(
			twinTiles,
			[TileTypeEnum.unavailable] )
