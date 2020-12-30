from typing import List, Dict
from core.enums.caverna_enums import TileTypeEnum


class TileRequisiteDefault(object):
    def assign(
            self,
            source: Dict[TileTypeEnum, List[TileTypeEnum]]) -> Dict[TileTypeEnum, List[TileTypeEnum]]:
        if source is None:
            raise ValueError("Source cannot be None")

        source.clear()
        source.update(
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
                TileTypeEnum.pasture: [TileTypeEnum.meadow],
                TileTypeEnum.pastureTwin: [TileTypeEnum.meadow],
                TileTypeEnum.furnishedCavern: [TileTypeEnum.cavern],
                TileTypeEnum.furnishedDwelling: [TileTypeEnum.cavern],
                TileTypeEnum.oreMine: [TileTypeEnum.tunnel],
                TileTypeEnum.oreMineDeepTunnelTwin: [TileTypeEnum.tunnel],
                TileTypeEnum.rubyMine: [TileTypeEnum.tunnel, TileTypeEnum.deepTunnel]}
        )

        return source
