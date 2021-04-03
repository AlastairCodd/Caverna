from abc import ABCMeta, abstractmethod
from typing import Dict, List, Callable
import math

from common.entities.point_lookup import PointLookup
from common.entities.tile_entity import TileEntity
from common.entities.tile_twin_placement_lookup import TileTwinPlacementLookup
from common.services.tile_service import TileService
from core.baseClasses.base_effect import BaseEffect
from core.baseClasses.base_tile import BaseSpecificTile
from core.constants import resource_types, tile_ids
from core.enums.caverna_enums import ResourceTypeEnum, TileColourEnum
from core.repositories.base_player_repository import BasePlayerRepository
from buisness_logic.effects import *


class BaseConditionalPointTile(BaseSpecificTile, metaclass=ABCMeta):
    def __init__(
            self,
            name: str,
            tile_id: int,
            base_points: int = 0,
            cost: Dict[ResourceTypeEnum, int] = None,
            effects: List[BaseEffect] = None):
        if effects is None:
            effects = []
        if cost is None:
            cost = {}

        BaseSpecificTile.__init__(
            self,
            name,
            tile_id,
            base_points=base_points,
            cost=cost,
            effects=effects,
            colour=TileColourEnum.Yellow)

    @abstractmethod
    def get_conditional_point(
            self,
            player: BasePlayerRepository,
            tile_entity: TileEntity) -> PointLookup:
        pass

    @abstractmethod
    def get_conditional_point_description(self) -> str:
        pass


class WeavingParlorTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "Weaving Parlor", tile_ids.WeavingParlorTileId,
            cost={ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 1},
            effects=[resource_effects.ReceiveProportionalOnPurchaseEffect(
                receive={ResourceTypeEnum.food: 1},
                proportional_to={ResourceTypeEnum.sheep: 1})])

    def get_conditional_point(
            self,
            player: BasePlayerRepository,
            tile_entity: TileEntity) -> PointLookup:
        if player is None:
            raise ValueError(str(player))
        return PointLookup(math.floor(player.resources[ResourceTypeEnum.sheep] / 2))

    def get_conditional_point_description(self) -> str:
        result: str = "One point per two sheep"
        return result


class MilkingParlorTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "Milking Parlor", tile_ids.MilkingParlorTileId,
            cost={ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 2},
            effects=[resource_effects.ReceiveProportionalOnPurchaseEffect(
                receive={ResourceTypeEnum.food: 1},
                proportional_to={ResourceTypeEnum.cow: 1})])

    def get_conditional_point(
            self,
            player: BasePlayerRepository,
            tile_entity: TileEntity) -> PointLookup:
        if player is None:
            raise ValueError(str(player))
        return PointLookup(player.resources[ResourceTypeEnum.cow])

    def get_conditional_point_description(self) -> str:
        result: str = "One point per cow"
        return result


class StateParlorTile(BaseConditionalPointTile):
    def __init__(self):
        self._tile_service: TileService = TileService()
        BaseConditionalPointTile.__init__(
            self, "State Parlor", tile_ids.StateParlorTileId,
            cost={ResourceTypeEnum.wood: 3, ResourceTypeEnum.coin: 5}, effects=[
                # TODO
            ])

    def get_conditional_point(
            self,
            player: BasePlayerRepository,
            tile_entity: TileEntity) -> PointLookup:
        if player is None:
            raise ValueError(str(player))

        adjacent_tile_locations: List[TileTwinPlacementLookup] = self._tile_service.get_adjacent_tiles(
            player,
            tile_entity.id)

        extraction_method: Callable[[TileTwinPlacementLookup], int] = lambda location_direction_pair: location_direction_pair[0]
        adjacent_tiles = [
            player.get_specific_tile_at_location(t)
            for t
            in map(extraction_method, adjacent_tile_locations)]
        number_of_adjacent_dwellings = len([d for d in adjacent_tiles if d.is_dwelling])
        result = 4 * number_of_adjacent_dwellings
        return PointLookup(result)

    def get_conditional_point_description(self) -> str:
        result: str = "Four points per adjacent dwelling tile"
        return result


class StoneStorageTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "Stone Storage", tile_ids.StoneStorageTileId,
            cost={ResourceTypeEnum.wood: 3, ResourceTypeEnum.ore: 1})

    def get_conditional_point(
            self,
            player: BasePlayerRepository,
            tile_entity: TileEntity) -> PointLookup:
        if player is None:
            raise ValueError(str(player))
        return PointLookup(player.resources[ResourceTypeEnum.stone])

    def get_conditional_point_description(self) -> str:
        result: str = "One point per stone"
        return result


class OreStorageTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "Ore Storage", tile_ids.OreStorageTileId,
            cost={ResourceTypeEnum.wood: 1, ResourceTypeEnum.ore: 2})

    def get_conditional_point(
            self,
            player: BasePlayerRepository,
            tile_entity: TileEntity) -> PointLookup:
        if player is None:
            raise ValueError(str(player))
        return PointLookup(math.floor(player.resources[ResourceTypeEnum.ore] / 2))

    def get_conditional_point_description(self) -> str:
        result: str = "One point per two ore"
        return result


class MainStorageTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "Main Storage", tile_ids.MainStorageTileId,
            cost={ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 1})

    def get_conditional_point(
            self,
            player: BasePlayerRepository,
            tile_entity: TileEntity) -> PointLookup:
        if player is None:
            raise ValueError(str(player))
        return PointLookup(len([t for t in player.tiles.values() if t.colour == TileColourEnum.Yellow]))

    def get_conditional_point_description(self) -> str:
        result: str = "Two points per yellow tile"
        return result


class WeaponStorageTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "Weapon Storage", tile_ids.WeaponStorageTileId,
            cost={ResourceTypeEnum.wood: 3, ResourceTypeEnum.stone: 2})

    def get_conditional_point(
            self,
            player: BasePlayerRepository,
            tile_entity: TileEntity) -> PointLookup:
        if player is None:
            raise ValueError(str(player))
        return PointLookup(len([d for d in player.dwarves if d.has_weapon]))

    def get_conditional_point_description(self) -> str:
        result: str = "Three points per dwarf with a weapon"
        return result


class SuppliesStorageTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "Supplies Storage", tile_ids.SuppliesStorageTileId,
            cost={ResourceTypeEnum.food: 3, ResourceTypeEnum.wood: 1})

    def get_conditional_point(
            self,
            player: BasePlayerRepository,
            tile_entity: TileEntity) -> PointLookup:
        if player is None:
            raise ValueError(str(player))
        if all([d.has_weapon for d in player.dwarves]):
            result = 8
        else:
            result = 0
        return PointLookup(result)

    def get_conditional_point_description(self) -> str:
        result: str = "Eight points per if all dwarves have weapons"
        return result


class BroomChamberTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "Broom Chamber", tile_ids.BroomChamberTileId,
            cost={ResourceTypeEnum.wood: 1})

    def get_conditional_point(
            self,
            player: BasePlayerRepository,
            tile_entity: TileEntity) -> PointLookup:
        if player is None:
            raise ValueError(str(player))

        number_of_dwarfs = len(player.dwarves)
        if number_of_dwarfs == 5:
            return PointLookup(5)
        elif number_of_dwarfs == 6:
            return PointLookup(10)
        else:
            return PointLookup()

    def get_conditional_point_description(self) -> str:
        result: str = "5 points if player has 5 dwarves, 10 points if player has 6 dwarves"
        return result


class TreasureChamberTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "Treasure Chamber", tile_ids.TreasureChamberTileId,
            cost={ResourceTypeEnum.wood: 1, ResourceTypeEnum.stone: 1})

    def get_conditional_point(
            self,
            player: BasePlayerRepository,
            tile_entity: TileEntity) -> PointLookup:
        if player is None:
            raise ValueError(str(player))
        return PointLookup(player.resources[ResourceTypeEnum.ruby])

    def get_conditional_point_description(self) -> str:
        result: str = "One point per ruby"
        return result


class FoodChamberTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "Food Chamber", tile_ids.FoodChamberTileId,
            cost={ResourceTypeEnum.wood: 2, ResourceTypeEnum.veg: 2})

    def get_conditional_point(
            self,
            player: BasePlayerRepository,
            tile_entity: TileEntity) -> PointLookup:
        if player is None:
            raise ValueError(str(player))

        result = min(player.resources[ResourceTypeEnum.veg], player.resources[ResourceTypeEnum.grain]) * 2
        return PointLookup(result)

    def get_conditional_point_description(self) -> str:
        result: str = "Two points per pair of veg and grain"
        return result


class PrayerChamberTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "Prayer Chamber", tile_ids.PrayerChamberTileId,
            cost={ResourceTypeEnum.wood: 2})

    def get_conditional_point(
            self,
            player: BasePlayerRepository,
            tile_entity: TileEntity) -> PointLookup:
        if player is None:
            raise ValueError(str(player))
        if any([d.has_weapon for d in player.dwarves]):
            result = 0
        else:
            result = 8
        return PointLookup(result)

    def get_conditional_point_description(self) -> str:
        result: str = "Eight points per if no dwarves have weapons"
        return result


class WritingChamberTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "Writing Chamber", tile_ids.WritingChamberTileId,
            cost={ResourceTypeEnum.stone: 2})

    def get_conditional_point(
            self,
            player: BasePlayerRepository,
            tile_entity: TileEntity) -> PointLookup:
        return PointLookup(0, 0, 7)

    def get_conditional_point_description(self) -> str:
        result: str = "Prevents up to seven negative points"
        return result


class FodderChamberTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "Fodder Chamber", tile_ids.FodderChamberTileId,
            cost={ResourceTypeEnum.grain: 2, ResourceTypeEnum.stone: 1})

    def get_conditional_point(
            self,
            player: BasePlayerRepository,
            tile_entity: TileEntity) -> PointLookup:
        if player is None:
            raise ValueError(str(player))
        players_farm_animals: List[int] = [player.resources[x] for x in resource_types.farm_animals]
        number_of_farm_animals: int = sum(players_farm_animals)
        result: int = math.floor(number_of_farm_animals / 3)

        return PointLookup(result)

    def get_conditional_point_description(self) -> str:
        result: str = "One points per three farm animals"
        return result