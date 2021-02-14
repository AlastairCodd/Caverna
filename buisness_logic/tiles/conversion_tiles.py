from core.baseClasses.base_tile import BaseSpecificTile
from core.constants import tile_ids, resource_types
from core.enums.caverna_enums import ResourceTypeEnum
from buisness_logic.effects import *


class TraderTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Trader", tile_ids.TraderTileId,
            base_points=2,
            cost={ResourceTypeEnum.wood: 2},
            effects=[conversion_effects.ConvertEffect(
                {ResourceTypeEnum.coin: 2},
                {ResourceTypeEnum.stone: 1, ResourceTypeEnum.wood: 1, ResourceTypeEnum.ore: 1})])


class SlaughteringCaveTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Slaughtering Cave", tile_ids.SlaughteringCaveTileId,
            base_points=2,
            cost={ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 2},
            effects=[resource_effects.ReceiveOnConvertFromEffect({ResourceTypeEnum.food: 1}, animal) for animal in resource_types.farm_animals])


class CookingCaveTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Cooking Cave", tile_ids.CookingCaveTileId,
            base_points=2,
            cost={ResourceTypeEnum.stone: 2},
            effects=[conversion_effects.ConvertEffect(
                {ResourceTypeEnum.veg: 1, ResourceTypeEnum.grain: 1},
                {ResourceTypeEnum.food: 5})])


# class PeacefulCaveTile(BaseSpecificTile):
#     def __init__(self):
#         BaseSpecificTile.__init__(
#             self, "Peaceful Cave", tile_ids.PeacefulCaveTileId,
#             base_points=2,
#             cost={ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 1},
#             effects=[# TODO: Workout whatever this i])


class HuntingParlorTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Hunting Parlor", tile_ids.HuntingParlorTileId,
            base_points=1,
            cost={ResourceTypeEnum.wood: 2},
            effects=[conversion_effects.ConvertEffect(
                {ResourceTypeEnum.boar: 2},
                {ResourceTypeEnum.coin: 2, ResourceTypeEnum.food: 2})])


class BeerParlorTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Beer Parlor", tile_ids.BeerParlorTileId,
            base_points=3,
            cost={ResourceTypeEnum.wood: 2},
            effects=[
                conversion_effects.ConvertEffect(
                    {ResourceTypeEnum.grain: 2},
                    {ResourceTypeEnum.coin: 3}),
                conversion_effects.ConvertEffect(
                    {ResourceTypeEnum.grain: 2},
                    {ResourceTypeEnum.food: 4})])


class BlacksmithingParlorTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Blacksmithing Parlor", tile_ids.BlacksmithingParlorTileId,
            base_points=2,
            cost={ResourceTypeEnum.ore: 3},
            effects=[conversion_effects.ConvertEffect(
                {ResourceTypeEnum.ore: 1, ResourceTypeEnum.ruby: 1},
                {ResourceTypeEnum.coin: 2, ResourceTypeEnum.food: 1})])


class SparePartStorageTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Spare Part Storage", tile_ids.SparePartStorageTileId,
            base_points=0,
            cost={ResourceTypeEnum.wood: 2},
            effects=[conversion_effects.ConvertEffect(
                {ResourceTypeEnum.stone: 1, ResourceTypeEnum.wood: 1, ResourceTypeEnum.ore: 1},
                {ResourceTypeEnum.coin: 2})])
