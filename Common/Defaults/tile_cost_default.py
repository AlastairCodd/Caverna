from typing import Dict

from core.enums.caverna_enums import TileTypeEnum, ResourceTypeEnum


class TileCostDefault(object):
    # TODO: Use in tile service??
    def assign(
            self,
            current_requisites: Dict[TileTypeEnum, Dict[ResourceTypeEnum, int]]) -> Dict[TileTypeEnum, Dict[ResourceTypeEnum, int]]:
        if current_requisites is None:
            raise ValueError("currentRequisites")

        current_requisites.clear()
        current_requisites.update({TileTypeEnum.pasture: {ResourceTypeEnum.wood: 2}, TileTypeEnum.pastureTwin: {ResourceTypeEnum.wood: 4}})

        return current_requisites
