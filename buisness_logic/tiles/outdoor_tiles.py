from buisness_logic.effects.allow_farming_effect import AllowFarmingEffect
from buisness_logic.effects.animal_storage_effects import StoreAnyAnimalEffect
from core.baseClasses.base_tile import BaseTile, BaseTwinTile
from core.enums.caverna_enums import TileTypeEnum, ResourceTypeEnum


class FieldTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Field", 100,
            TileTypeEnum.field,
            effects=[AllowFarmingEffect()])


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
            cost={ResourceTypeEnum.wood: 2},
            effects=[StoreAnyAnimalEffect(2)])


class PastureTwinTile(BaseTwinTile):
    def __init__(self):
        BaseTwinTile.__init__(
            self, "Large Pasture", 104,
            TileTypeEnum.pastureTwin,
            base_points=4,
            cost={ResourceTypeEnum.wood: 4},
            effects=[StoreAnyAnimalEffect(4)])
