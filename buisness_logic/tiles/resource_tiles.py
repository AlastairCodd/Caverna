from buisness_logic.effects import *
from common.entities.tile_entity import TileEntity
from core.baseClasses.base_tile import BaseSpecificTile
from core.constants import tile_ids
from core.enums.caverna_enums import ResourceTypeEnum, TileTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository


class MinerTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Miner", tile_ids.MinerTileId,
            base_points=3,
            cost={ResourceTypeEnum.wood: 1, ResourceTypeEnum.stone: 1},
            effects=[resource_effects.ReceiveConditionallyAtStartOfTurnEffect(
                {ResourceTypeEnum.donkey: 1},
                self._condition)])

    def _condition(
            self,
            player: BasePlayerRepository) -> int:
        if player is None:
            raise ValueError("Player may not be null")

        number_of_donkeys_in_mines: int = 0
        tile: TileEntity
        for tile in player.tiles:
            if tile.tile_type == TileTypeEnum.oreMineDeepTunnelTwin and \
                    tile.animal_type == ResourceTypeEnum.donkey:
                number_of_donkeys_in_mines += tile.number_of_animals
        return number_of_donkeys_in_mines


class WoodSupplierTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Wood Supplier", tile_ids.WoodSupplierTileId,
            base_points=2,
            cost={ResourceTypeEnum.stone: 1},
            effects=[resource_effects.ReceiveForTurnsEffect({ResourceTypeEnum.wood: 1}, 7)])


class StoneSupplierTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Stone Supplier", tile_ids.StoneSupplierTileId,
            base_points=1,
            cost={ResourceTypeEnum.wood: 1},
            effects=[resource_effects.ReceiveForTurnsEffect({ResourceTypeEnum.stone: 1}, 5)])


class RubySupplierTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Ruby Supplier", tile_ids.RubySupplierTileId,
            base_points=2,
            cost={ResourceTypeEnum.stone: 2, ResourceTypeEnum.wood: 2},
            effects=[resource_effects.ReceiveForTurnsEffect({ResourceTypeEnum.ruby: 1}, 4)])
