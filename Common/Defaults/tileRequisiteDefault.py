from typing import List, Dict
from Core.cavernaEnums import TileTypeEnum

class TileRequisiteDefault(object):
	def assign(self, currentRequisites: Dict[TileTypeEnum, List[TileTypeEnum]]) -> Dict[TileTypeEnum, List[TileTypeEnum]]:
		if currentRequisites is None: raise ValueError("currentRequisites")
		
		currentRequisites.clear()
		currentRequisites.update(
			{
				TileTypeEnum.unavailable: [],
				TileTypeEnum.forest: [],
				TileTypeEnum.underground: [],
				TileTypeEnum.meadow: [TileTypeEnum.forest],
				TileTypeEnum.field: [TileTypeEnum.forest],
				TileTypeEnum.meadowFieldTwin: [TileTypeEnum.forest],
				TileTypeEnum.cavern: [TileTypeEnum.underground],
				TileTypeEnum.tunnel: [TileTypeEnum.underground],
				TileTypeEnum.deepTunnel: [TileTypeEnum.tunnel],
				TileTypeEnum.cavernTunnelTwin: [TileTypeEnum.underground],
				TileTypeEnum.cavernCavernTwin: [TileTypeEnum.underground],
				TileTypeEnum.pasture: [TileTypeEnum.field],
				TileTypeEnum.pastureTwin: [TileTypeEnum.field],
				TileTypeEnum.furnishedCavern: [TileTypeEnum.cavern],
				TileTypeEnum.furnishedDwelling: [TileTypeEnum.cavern],
				TileTypeEnum.oreMineDeepTunnelTwin: [TileTypeEnum.tunnel],
				TileTypeEnum.rubyMine: [TileTypeEnum.tunnel, TileTypeEnum.deepTunnel] }
			)
		return currentRequisites