from buisness_logic.effects import animal_storage_effects
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum, TileTypeEnum


class CavernTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Cavern", 201,
            TileTypeEnum.cavern)


class TunnelTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Tunnel", 211,
            TileTypeEnum.tunnel)


class DeepTunnelTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Deep Tunnel", 212,
            TileTypeEnum.deepTunnel)


class OreMineTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Ore Mine", 221,
            TileTypeEnum.oreMine,
            base_points=3,
            effects=[animal_storage_effects.StoreSpecificAnimalEffect({ResourceTypeEnum.donkey: 1})])


class RubyMineTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Ruby Mine", 222,
            TileTypeEnum.rubyMine,
            base_points=4,
            effects=[animal_storage_effects.StoreSpecificAnimalEffect({ResourceTypeEnum.donkey: 1})])