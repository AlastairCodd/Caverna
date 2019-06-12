from typing import Dict, List
from player import Player
from Core.baseEffect import BaseEffect
from Core.cavernaEnums import TileTypeEnum
from Common.TileTwinDefault import TileTwinDefault

class BaseBoardEffect(BaseEffect):
	def Invoke(self, source: Dict[TileTypeEnum, List[TileTypeEnum]]) -> Dict[TileTypeEnum, List[TileTypeEnum]]:
		raise NotImplementedException("base population effect class")
	
class FurnishTunnelsEffect(BaseBoardEffect):
	def Invoke(self, source: Dict[TileTypeEnum, List[TileTypeEnum]]) -> Dict[TileTypeEnum, List[TileTypeEnum]]:
		if source is None:
			raise ValueError()
		
		source[TileTypeEnum.furnishedCavern].extend([TileTypeEnum.tunnel, TileTypeEnum.deepTunnel]
		source[TileTypeEnum.furnishedDwelling].extend([TileTypeEnum.tunnel, TileTypeEnum.deepTunnel]
		return source
		
class TwinTilesOverhangEffect(BaseBoardEffect):
	def Invoke(self, source: Dict[TileTypeEnum, List[TileTypeEnum]]) -> Dict[TileTypeEnum, List[TileTypeEnum]]:
		if source is None:
			raise ValueError()
			
		twinDefault = TileTwinDefault.TileTwinDefault()
		twinTiles = twinDefault.Assign( [] )
		
		for x in source if x in twinTiles:
			source[x].add( TileTypeEnum.unavailable )
			
		return source