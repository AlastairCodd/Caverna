from buisness_logic.effects import *
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum


class MinerTile(BaseTile):
    def __init__(self):
        super().__init__(
            "Miner", 15, False, 3,
            {ResourceTypeEnum.wood: 1, ResourceTypeEnum.stone: 1},
            [resource_effects.ReceiveConditional({ResourceTypeEnum.donkey: 1}, {ResourceTypeEnum.ore: 1})])


class WoodSupplierTile(BaseTile):
    def __init__(self):
        super().__init__(
            "Wood Supplier", 18, False, 2,
            {ResourceTypeEnum.stone: 1},
            [resource_effects.ReceiveForTurns({ResourceTypeEnum.wood: 1}, 7)])


class StoneSupplierTile(BaseTile):
    def __init__(self):
        super().__init__(
            "Stone Supplier", 19, False, 1,
            {ResourceTypeEnum.wood: 1},
            [resource_effects.ReceiveForTurns({ResourceTypeEnum.stone: 1}, 5)])


class RubySupplierTile(BaseTile):
    def __init__(self):
        super().__init__(
            "Ruby Supplier", 20, False, 2,
            {ResourceTypeEnum.stone: 2, ResourceTypeEnum.wood: 2},
            [resource_effects.ReceiveForTurns({ResourceTypeEnum.ruby: 1}, 4)])
