from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum
from common.entities import weapon
from buisness_logic.effects import *


class TraderTile(BaseTile):
    def __init__(self):
        super().__init__(
            "Trader", 17, False, 2,
            {ResourceTypeEnum.wood: 2},
            [conversion_effects.Convert(
                {ResourceTypeEnum.coin: 2},
                {ResourceTypeEnum.stone: 1, ResourceTypeEnum.wood: 1, ResourceTypeEnum.ore: 1})])


class SlaughteringCaveTile(BaseTile):
    def __init__(self):
        super().__init__(
            "Slaughtering Cave", 24, False, 2,
            {ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 2},
            [conversion_effects.ChangeFoodConversionRate({
                {ResourceTypeEnum.donkey: 1}: 2,
                {ResourceTypeEnum.sheep: 1}: 2,
                {ResourceTypeEnum.boar: 1}: 3,
                {ResourceTypeEnum.cow: 1}: 4,
                {ResourceTypeEnum.donkey: 2}: 4})])


class CookingCaveTile(BaseTile):
    def __init__(self):
        super().__init__(
            "Cooking Cave", 25, False, 2,
            {ResourceTypeEnum.stone: 2},
            [conversion_effects.Convert(
                {ResourceTypeEnum.veg: 1, ResourceTypeEnum.grain: 1},
                {ResourceTypeEnum.food: 5})])


class PeacefulCaveTile(BaseTile):
    def __init__(self):
        super().__init__(
            "Peaceful Cave", 29, False, 2,
            {ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 1},
            [conversion_effects.ConvertProportional(
                [weapon.Weapon],
                [ResourceTypeEnum.food],
                lambda x: x.level())])


class HuntingParlorTile(BaseTile):
    def __init__(self):
        super().__init__(
            "Hunting Parlor", 33, False, 1,
            {ResourceTypeEnum.wood: 2},
            [conversion_effects.Convert(
                {ResourceTypeEnum.boar: 2},
                {ResourceTypeEnum.coin: 2, ResourceTypeEnum.food: 2})])


class BeerParlorTile(BaseTile):
    def __init__(self):
        super().__init__(
            "Beer Parlor", 34, False, 3,
            {ResourceTypeEnum.wood: 2},
            [conversion_effects.Convert(
                {ResourceTypeEnum.grain: 2},
                {ResourceTypeEnum.coin: 3}),
                conversion_effects.Convert(
                    {ResourceTypeEnum.grain: 2},
                    {ResourceTypeEnum.food: 4})])


class BlacksmithingPalorTile(BaseTile):
    def __init__(self):
        super().__init__(
            "Blacksmithing Palor", 35, False, 2,
            {ResourceTypeEnum.ore: 3},
            [conversion_effects.Convert(
                {ResourceTypeEnum.ore: 1, ResourceTypeEnum.ruby: 1},
                {ResourceTypeEnum.coin: 2, ResourceTypeEnum.food: 1})])


class SparePartStorageTile(BaseTile):
    def __init__(self):
        super().__init__(
            "Spare Part Storage", 38, False, 0,
            {ResourceTypeEnum.wood: 2},
            [conversion_effects.Convert(
                {ResourceTypeEnum.stone: 1, ResourceTypeEnum.wood: 1, ResourceTypeEnum.ore: 1},
                {ResourceTypeEnum.coin: 2})])
