from buisness_logic.effects import purchase_effects, resource_effects
from core.enums.caverna_enums import ResourceTypeEnum, TileTypeEnum
from core.baseClasses.base_tile import BaseTile
from common.entities import weapon


class CarpenterTile(BaseTile):
    def __init__(self):
        super().__init__(
            "Carpenter", 12,
            cost={ResourceTypeEnum.stone: 1},
            effects=[purchase_effects.DecreasePrice({ResourceTypeEnum.wood: 1}, BaseTile)])


class StoneCarverTile(BaseTile):
    def __init__(self):
        super().__init__(
            "Stone Carver", 13, base_points=1,
            cost={ResourceTypeEnum.wood: 1},
            effects=[
                resource_effects.Receive({ResourceTypeEnum.stone: 2}),
                purchase_effects.DecreasePrice({ResourceTypeEnum.stone: 1}, BaseTile)])


class BlacksmithTile(BaseTile):
    def __init__(self):
        super().__init__(
            "Blacksmith", 14, base_points=3,
            cost={ResourceTypeEnum.wood: 1, ResourceTypeEnum.stone: 2},
            effects=[
                resource_effects.Receive({ResourceTypeEnum.ore: 2}),
                purchase_effects.DecreasePrice({ResourceTypeEnum.ore: 2}, weapon.Weapon)])


class BuilderTile(BaseTile):
    def __init__(self):
        super().__init__(
            "Builder", 16, base_points=2,
            cost={ResourceTypeEnum.stone: 1},
            effects=[purchase_effects.DecreasePrice({ResourceTypeEnum.ore: 2}, weapon.Weapon)])
