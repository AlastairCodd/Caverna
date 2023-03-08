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
    def append_formatted_conditional_points(self, text) -> None:
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
        return PointLookup(player.resources[ResourceTypeEnum.sheep])

    def append_formatted_conditional_points(self, text) -> None:
        text.append(("", "is worth "))
        text.append(("class:point_count", "1"))
        text.append(("", " point per "))
        text.append(("", "sheep"))


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

    def append_formatted_conditional_points(self, text) -> None:
        text.append(("", "is worth "))
        text.append(("class:point_count", "1"))
        text.append(("", " point per "))
        text.append(("", "cow"))


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

    def append_formatted_conditional_points(self, text) -> None:
        text.append(("", "is worth "))
        text.append(("class:point_count", "4"))
        text.append(("", " points per "))
        text.append(("", "dwelling"))
        text.append(("", " adjacent to this tile"))


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

    def append_formatted_conditional_points(self, text) -> None:
        text.append(("", "is worth "))
        text.append(("class:point_count", "1"))
        text.append(("", " point per "))
        text.append(("", "stone"))


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

    def append_formatted_conditional_points(self, text) -> None:
        text.append(("", "is worth "))
        text.append(("class:point_count", "1"))
        text.append(("", " point for every "))
        text.append(("class:count", "2"))
        text.append(("", " ore"))


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

    def append_formatted_conditional_points(self, text) -> None:
        text.append(("", "is worth "))
        text.append(("class:point_count", "1"))
        text.append(("", " point for every "))
        text.append(("", "yellow"))
        text.append(("", " tile"))
        text.append(("", " (including this)"))


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

    def append_formatted_conditional_points(self, text) -> None:
        text.append(("", "is worth "))
        text.append(("class:point_count", "3"))
        text.append(("", " points "))
        text.append(("class:count", "for each"))
        text.append(("", " "))
        text.append(("", "dwarf"))
        text.append(("", " with a weapon"))


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

    def append_formatted_conditional_points(self, text) -> None:
        text.append(("", "is worth "))
        text.append(("class:point_count", "8"))
        text.append(("", " points if and only if "))
        text.append(("class:count", "every"))
        text.append(("", " "))
        text.append(("", "dwarf"))
        text.append(("", " has a weapon"))


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

    def append_formatted_conditional_points(self, text) -> None:
        text.append(("", "is worth "))
        text.append(("class:point_count", "5"))
        text.append(("", " points if you have "))
        text.append(("class:count", "5"))
        text.append(("", " "))
        text.append(("", "dwarves"))
        text.append(("", " or "))
        text.append(("class:point_count", "10"))
        text.append(("", " points if you have "))
        text.append(("class:count", "6"))
        text.append(("", " "))
        text.append(("", "dwarves"))


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

    def append_formatted_conditional_points(self, text) -> None:
        text.append(("", "is worth "))
        text.append(("class:point_count", "1"))
        text.append(("", " point per "))
        text.append(("", "ruby"))


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

    def append_formatted_conditional_points(self, text) -> None:
        text.append(("", "is worth "))
        text.append(("class:point_count", "1"))
        text.append(("", " point per pair of "))
        text.append(("", "vegetable and grain"))


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

    def append_formatted_conditional_points(self, text) -> None:
        text.append(("", "is worth "))
        text.append(("class:point_count", "8"))
        text.append(("", " points if and only if "))
        text.append(("class:count", "no"))
        text.append(("", " "))
        text.append(("", "dwarves"))
        text.append(("", " have weapons"))


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

    def append_formatted_conditional_points(self, text) -> None:
        text.append(("", "negates up to "))
        text.append(("class:point_count", "7"))
        text.append(("", " negative points"))


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

    def append_formatted_conditional_points(self, text) -> None:
        text.append(("", "is worth "))
        text.append(("class:point_count", "1"))
        text.append(("", " point for every "))
        text.append(("class:count", "3"))
        text.append(("", " farm animals"))
