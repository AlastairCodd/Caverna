from typing import List
from core.enums.caverna_enums import TileTypeEnum


class TileTwinDefault(object):
    def assign(
            self,
            current_tiles: List[TileTypeEnum]) -> List[TileTypeEnum]:
        if current_tiles is None:
            raise ValueError()

        current_tiles.clear()
        current_tiles.extend([
            TileTypeEnum.meadowFieldTwin,
            TileTypeEnum.cavernTunnelTwin,
            TileTypeEnum.cavernCavernTwin,
            TileTypeEnum.pastureTwin,
            TileTypeEnum.oreMineDeepTunnelTwin])
        return current_tiles
