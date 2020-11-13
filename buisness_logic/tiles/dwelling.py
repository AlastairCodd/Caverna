from abc import ABCMeta
from typing import Dict, List

from core.baseClasses.base_effect import BaseEffect
from core.baseClasses.base_tile import BaseSpecificTile
from core.constants import tile_ids
from core.enums.caverna_enums import ResourceTypeEnum, TileColourEnum, TileTypeEnum
from buisness_logic.effects import population_effects, animal_storage_effects


class BaseDwelling(BaseSpecificTile, metaclass=ABCMeta):
    def __init__(
            self,
            name: str,
            tile_id: int,
            base_points: int,
            cost: Dict[ResourceTypeEnum, int],
            effects: List[BaseEffect]):
        BaseSpecificTile.__init__(
            self,
            name,
            tile_id,
            TileTypeEnum.furnishedDwelling,
            base_points,
            cost,
            effects,
            TileColourEnum.Green
        )


class Dwelling(BaseDwelling):
    def __init__(self):
        BaseDwelling.__init__(
            self, "Dwelling", tile_ids.DwellingTileId, 3,
            {ResourceTypeEnum.wood: 4, ResourceTypeEnum.stone: 3},
            [population_effects.IncreasePopulationCapacityEffect(1)])


class SimpleStoneDwelling(BaseDwelling):
    def __init__(self):
        BaseDwelling.__init__(
            self, "Simple Dwelling (stone)", tile_ids.SimpleDwellingStoneTileId, 0,
            {ResourceTypeEnum.wood: 4, ResourceTypeEnum.stone: 2},
            [population_effects.IncreasePopulationCapacityEffect(1)])


class SimpleWoodDwelling(BaseDwelling):
    def __init__(self):
        BaseDwelling.__init__(
            self, "Simple Dwelling (wood)", tile_ids.SimpleDwellingWoodTileId, 0,
            {ResourceTypeEnum.wood: 3, ResourceTypeEnum.stone: 3},
            [population_effects.IncreasePopulationCapacityEffect(1)])


class MixedDwelling(BaseDwelling):
    def __init__(self):
        BaseDwelling.__init__(
            self, "Mixed Dwelling", tile_ids.MixedDwellingTileId, 4,
            {ResourceTypeEnum.wood: 5, ResourceTypeEnum.stone: 4},
            [population_effects.IncreasePopulationCapacityEffect(1), animal_storage_effects.StoreAny(2)])


class CoupleDwelling(BaseDwelling):
    def __init__(self):
        BaseDwelling.__init__(
            self, "Couple Dwelling", tile_ids.CoupleDwellingTileId, 5,
            {ResourceTypeEnum.wood: 8, ResourceTypeEnum.stone: 6},
            [population_effects.IncreasePopulationCapacityEffect(2)])


class AdditionalDwelling(BaseDwelling):
    def __init__(self):
        BaseDwelling.__init__(
            self, "Additional Dwelling", tile_ids.AdditionalDwellingTileId, 5,
            {ResourceTypeEnum.wood: 4, ResourceTypeEnum.stone: 3},
            [population_effects.IncreasePopulationMaximumEffect(),
             population_effects.IncreasePopulationCapacityEffect(1)])


class EntryLevelDwelling(BaseDwelling):
    def __init__(self) -> None:
        BaseDwelling.__init__(
            self, "Entry Level Dwelling", tile_ids.EntryLevelDwellingTileId, 0, {},
            [population_effects.IncreasePopulationCapacityEffect(2),
             animal_storage_effects.StoreAny(2)])