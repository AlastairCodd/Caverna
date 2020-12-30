from typing import List, Dict

from buisness_logic.actions.breed_animals_action import BreedAnimalsAction
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

        # TODO: apply animal resource calculation for this step

        number_of_donkeys_in_mines: int = 0
        # tile: TileEntity
        # for tile in player.tiles:
        #     if tile.tile_type == TileTypeEnum.oreMineDeepTunnelTwin and \
        #             tile.animal_type == ResourceTypeEnum.donkey:
        #         number_of_donkeys_in_mines += tile.number_of_animals
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


class DogSchoolTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Dog School", tile_ids.DogSchoolTileId,
            effects=[resource_effects.ReceiveWhenReceivingEffect(
                {ResourceTypeEnum.wood: 1},
                {ResourceTypeEnum.dog: 1})])


class QuarryTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Quarry", tile_ids.QuarryTileId,
            base_points=2,
            cost={ResourceTypeEnum.wood: 1},
            effects=[resource_effects.ReceiveWhenBreedingEffect(self._condition)])

    def _condition(
            self,
            newborn_animals: List[ResourceTypeEnum]) -> Dict[ResourceTypeEnum, int]:
        result: Dict[ResourceTypeEnum, int] = {ResourceTypeEnum.stone: 1} if ResourceTypeEnum.donkey in newborn_animals else {}
        return result


class BreedingCaveTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Breeding Cave", tile_ids.BreedingCaveTileId,
            base_points=2,
            cost={
                ResourceTypeEnum.grain: 1,
                ResourceTypeEnum.stone: 1},
            effects=[resource_effects.ReceiveWhenBreedingEffect(self._condition)])
        self._conversion_effect: Dict[int, int] = {
            1: 1,
            2: 2,
            3: 3,
            4: 5
        }

    def _condition(
            self,
            newborn_animals: List[ResourceTypeEnum]) -> Dict[ResourceTypeEnum, int]:
        number_of_newborn_animals: int = len(newborn_animals)
        amount_of_food: int = self._conversion_effect[number_of_newborn_animals]
        result: Dict[ResourceTypeEnum, int] = {ResourceTypeEnum.food: amount_of_food}
        return result


class SeamTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Seam", tile_ids.SeamTileId,
            base_points=1,
            cost={ResourceTypeEnum.stone: 2},
            effects=[resource_effects.ReceiveWhenReceivingEffect(
                {ResourceTypeEnum.ore: 1},
                {ResourceTypeEnum.stone: 1})])