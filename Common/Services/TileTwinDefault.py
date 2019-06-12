from typing import Dict
from Core.cavernaEnums import TileTypeEnum

class TileTwinDefault(object):

	def Assign(self, currentTiles: List[TileTypeEnum]) -> List[TileTypeEnum]:
		if currentTiles is None:
			raise ValueError()

		currentTiles.clear()
		currentTiles.extend( [
			TileTypeEnum.meadowFieldTwin,
			TileTypeEnum.cavernTunnelTwin,
			TileTypeEnum.cavernCavernTwin,
			TileTypeEnum.pastureTwin,
			TileTypeEnum.oreMineDeepTunnelTwin ] )
		return currentTiles