from core.baseClasses.base_tile import BaseSpecificTile
from core.constants import tile_ids
from core.enums.caverna_enums import ResourceTypeEnum
from common.entities import weapon
from buisness_logic.effects import *


class TraderTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Trader", tile_ids.TraderTileId,
            base_points=2,
            cost={ResourceTypeEnum.wood: 2},
            effects=[conversion_effects.Convert(
                {ResourceTypeEnum.coin: 2},
                {ResourceTypeEnum.stone: 1, ResourceTypeEnum.wood: 1, ResourceTypeEnum.ore: 1})])


class SlaughteringCaveTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Slaughtering Cave", tile_ids.SlaughteringCaveTileId,
            base_points=2,
            cost={ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 2},
            effects=[conversion_effects.ChangeFoodConversionRate({
                {ResourceTypeEnum.donkey: 1}: 2,
                {ResourceTypeEnum.sheep: 1}: 2,
                {ResourceTypeEnum.boar: 1}: 3,
                {ResourceTypeEnum.cow: 1}: 4,
                {ResourceTypeEnum.donkey: 2}: 4})])


class CookingCaveTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Cooking Cave", tile_ids.CookingCaveTileId,
            base_points=2,
            cost={ResourceTypeEnum.stone: 2},
            effects=[conversion_effects.Convert(
                {ResourceTypeEnum.veg: 1, ResourceTypeEnum.grain: 1},
                {ResourceTypeEnum.food: 5})])


class PeacefulCaveTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Peaceful Cave", tile_ids.PeacefulCaveTileId,
            base_points=2,
            cost={ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 1},
            effects=[conversion_effects.ConvertProportional(
                # TODO: Workout whatever this is
                [weapon.Weapon],
                [ResourceTypeEnum.food],
                lambda x: x.level())])


class HuntingParlorTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Hunting Parlor", tile_ids.HuntingParlorTileId,
            base_points=1,
            cost={ResourceTypeEnum.wood: 2},
            effects=[conversion_effects.Convert(
                {ResourceTypeEnum.boar: 2},
                {ResourceTypeEnum.coin: 2, ResourceTypeEnum.food: 2})])


class BeerParlorTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Beer Parlor", tile_ids.BeerParlorTileId,
            base_points=3,
            cost={ResourceTypeEnum.wood: 2},
            effects=[conversion_effects.Convert(
                {ResourceTypeEnum.grain: 2},
                {ResourceTypeEnum.coin: 3}),
                conversion_effects.Convert(
                    {ResourceTypeEnum.grain: 2},
                    {ResourceTypeEnum.food: 4})])


class BlacksmithingParlorTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Blacksmithing Parlor", tile_ids.BlacksmithingParlorTileId,
            base_points=2,
            cost={ResourceTypeEnum.ore: 3},
            effects=[conversion_effects.Convert(
                {ResourceTypeEnum.ore: 1, ResourceTypeEnum.ruby: 1},
                {ResourceTypeEnum.coin: 2, ResourceTypeEnum.food: 1})])


class SparePartStorageTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Spare Part Storage", tile_ids.SparePartStorageTileId,
            base_points=0,
            cost={ResourceTypeEnum.wood: 2},
            effects=[conversion_effects.Convert(
                {ResourceTypeEnum.stone: 1, ResourceTypeEnum.wood: 1, ResourceTypeEnum.ore: 1},
                {ResourceTypeEnum.coin: 2})])
