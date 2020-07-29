from buisness_logic.effects import *
from core.baseClasses.base_tile import BaseSpecificTile
from core.constants import tile_ids
from core.enums.caverna_enums import ResourceTypeEnum


class MinerTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Miner", tile_ids.MinerTileId,
            base_points=3,
            cost={ResourceTypeEnum.wood: 1, ResourceTypeEnum.stone: 1},
            effects=[resource_effects.ReceiveConditional({ResourceTypeEnum.donkey: 1}, lambda player: player.get_resources_of_type(ResourceTypeEnum.ore))])


class WoodSupplierTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Wood Supplier", tile_ids.WoodSupplierTileId,
            base_points=2,
            cost={ResourceTypeEnum.stone: 1},
            effects=[resource_effects.ReceiveForTurns({ResourceTypeEnum.wood: 1}, 7)])


class StoneSupplierTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Stone Supplier", tile_ids.StoneSupplierTileId,
            base_points=1,
            cost={ResourceTypeEnum.wood: 1},
            effects=[resource_effects.ReceiveForTurns({ResourceTypeEnum.stone: 1}, 5)])


class RubySupplierTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Ruby Supplier", tile_ids.RubySupplierTileId,
            base_points=2,
            cost={ResourceTypeEnum.stone: 2, ResourceTypeEnum.wood: 2},
            effects=[resource_effects.ReceiveForTurns({ResourceTypeEnum.ruby: 1}, 4)])
