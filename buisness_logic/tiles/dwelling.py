from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum, TileColourEnum
from buisness_logic.effects import population_effects, animal_storage_effects


class Dwelling(BaseTile):
    def __init__(self):
        super().__init__(
            "Dwelling", 0, True, 3,
            {ResourceTypeEnum.wood: 4, ResourceTypeEnum.stone: 3},
            [population_effects.IncreasePopulationCapEffect(1)],
            TileColourEnum.Green)


class SimpleStoneDwelling(BaseTile):
    def __init__(self):
        super().__init__(
            "Simple Dwelling (stone)", 1, True, 0,
            {ResourceTypeEnum.wood: 4, ResourceTypeEnum.stone: 2},
            [population_effects.IncreasePopulationCapEffect(1)],
            TileColourEnum.Green)


class SimpleWoodDwelling(BaseTile):
    def __init__(self):
        super().__init__(
            "Simple Dwelling (wood)", 2, True, 0,
            {ResourceTypeEnum.wood: 3, ResourceTypeEnum.stone: 3},
            [population_effects.IncreasePopulationCapEffect(1)],
            TileColourEnum.Green)


class MixedDwelling(BaseTile):
    def __init__(self):
        super().__init__(
            "Mixed Dwelling", 3, True, 4,
            {ResourceTypeEnum.wood: 5, ResourceTypeEnum.stone: 4},
            [population_effects.IncreasePopulationCapEffect(1), animal_storage_effects.StoreAny(2)],
            TileColourEnum.Green)


class CoupleDwelling(BaseTile):
    def __init__(self):
        super().__init__(
            "Couple Dwelling", 4, True, 5,
            {ResourceTypeEnum.wood: 8, ResourceTypeEnum.stone: 6},
            [population_effects.IncreasePopulationCapEffect(2)],
            TileColourEnum.Green)


class AdditionalDwelling(BaseTile):
    def __init__(self):
        super().__init__(
            "Couple Dwelling", 5, True, 5,
            {ResourceTypeEnum.wood: 4, ResourceTypeEnum.stone: 3},
            [population_effects.AllowSixthDwarfEffect()],
            TileColourEnum.Green)
