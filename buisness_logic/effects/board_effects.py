from typing import Dict, List
from core.baseClasses.base_effect import BaseEffect
from core.enums.caverna_enums import TileTypeEnum
from common.defaults.tile_twin_default import TileTwinDefault


class BaseBoardEffect(BaseEffect):
    def invoke(self, source: Dict[TileTypeEnum, List[TileTypeEnum]]) -> Dict[TileTypeEnum, List[TileTypeEnum]]:
        raise NotImplementedError("base board effect class")


class ChangeRequisiteEffect(BaseBoardEffect):
    def __init__(self, tiles: List[TileTypeEnum], new_requisites: List[TileTypeEnum]):
        if tiles is None:
            raise ValueError()
        if new_requisites is None:
            raise ValueError()

        self._tiles: List[TileTypeEnum] = tiles
        self._newRequisites: List[TileTypeEnum] = new_requisites
        super().__init__()

    def invoke(self, source: Dict[TileTypeEnum, List[TileTypeEnum]]) -> Dict[TileTypeEnum, List[TileTypeEnum]]:
        if source is None:
            raise ValueError()

        for tile in self._tiles:
            source[tile].extend(self._newRequisites)
        return source


class FurnishTunnelsEffect(ChangeRequisiteEffect):
    def __init__(self):
        super().__init__(
            [TileTypeEnum.furnishedCavern, TileTypeEnum.furnishedDwelling],
            [TileTypeEnum.tunnel, TileTypeEnum.deepTunnel])


class TwinTilesOverhangEffect(ChangeRequisiteEffect):
    def __init__(self):
        twin_default = TileTwinDefault()
        twin_tiles = twin_default.assign([])
        super().__init__(
            twin_tiles,
            [TileTypeEnum.unavailable])
