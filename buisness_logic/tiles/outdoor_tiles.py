from buisness_logic.effects import animal_storage_effects
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import TileTypeEnum


class FieldTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Field", 100,
            TileTypeEnum.field)


class MeadowTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Meadow", 101,
            TileTypeEnum.meadow)


class PastureTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Pasture", 103,
            TileTypeEnum.pasture,
            base_points=2,
            effects=[animal_storage_effects.StoreAny(2)])


class PastureTwinTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Large Pasture", 104,
            TileTypeEnum.pastureTwin,
            base_points=4,
            effects=[animal_storage_effects.StoreAny(4)])
