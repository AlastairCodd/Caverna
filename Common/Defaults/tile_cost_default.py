from typing import List, Dict
from core.enums.cavernaEnums import TileTypeEnum, ResourceTypeEnum

class TileCostDefault(object):
	def assign(self, currentRequisites: Dict[TileTypeEnum, Dict[ResourceTypeEnum, int]]) -> Dict[TileTypeEnum, Dict[ResourceTypeEnum, int]]:
		if currentRequisites is None: raise ValueError("currentRequisites")
		
		currentRequisites.clear()
		currentRequisites.update( { TileTypeEnum.pasture: {ResourceTypeEnum.wood: 2}, TileTypeEnum.pastureTwin: {ResourceTypeEnum.wood: 4} } )
        
		return currentRequisites