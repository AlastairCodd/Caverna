from buisness_logic.effects import animal_storage_effects
from core.baseClasses.base_tile import BaseTile
from core.constants import tile_ids
from core.enums.caverna_enums import ResourceTypeEnum, TileTypeEnum


class CavernTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Cavern", tile_ids.CavernTileId,
            TileTypeEnum.cavern)


class TunnelTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Tunnel", tile_ids.TunnelTileId,
            TileTypeEnum.tunnel)


class DeepTunnelTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Deep Tunnel", tile_ids.DeepTunnelTileId,
            TileTypeEnum.deepTunnel)


class OreMineTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Ore Mine", tile_ids.OreMineTileId,
            TileTypeEnum.oreMine,
            base_points=3,
            effects=[animal_storage_effects.StoreSpecificAnimalEffect({ResourceTypeEnum.donkey: 1})])


class RubyMineTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Ruby Mine", tile_ids.RubyMineTileId,
            TileTypeEnum.rubyMine,
            base_points=4,
            effects=[animal_storage_effects.StoreSpecificAnimalEffect({ResourceTypeEnum.donkey: 1})])