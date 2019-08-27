from abc import ABC, abstractmethod
from typing import Dict, List
import math

from common.entities.point_entity import PointEntity
from core.baseClasses.base_effect import BaseEffect
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum, TileColourEnum
from common.entities.player import Player
from common.defaults.farm_animal_resource_type_default import FarmAnimalResourceTypeDefault
from buisness_logic.effects import *


class BaseConditionalPointTile(BaseTile, ABC):
    def __init__(
            self,
            name: str,
            tile_id: int,
            is_dwelling: bool = False,
            base_points: int = 0,
            cost: Dict[ResourceTypeEnum, int] = None,
            effects: List[BaseEffect] = None):
        if effects is None:
            effects = []
        if cost is None:
            cost = {}

        BaseTile.__init__(self, name, tile_id, is_dwelling, base_points, cost, effects, TileColourEnum.Yellow)

    @abstractmethod
    def get_conditional_point(self, player: Player) -> PointEntity:
        pass


class WeavingParlorTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "Weaving Parlor", 30,
            cost={ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 1},
            effects=[resource_effects.ReceiveProportional(
                received={ResourceTypeEnum.food: 1},
                proportionalTo={ResourceTypeEnum.sheep: 1})])

    def get_conditional_point(self, player: Player) -> PointEntity:
        if player is None:
            raise ValueError(str(player))
        return PointEntity(player.resources[ResourceTypeEnum.sheep])


class MilkingParlorTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "Milking Parlor", 31,
            cost={ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 2},
            effects=[resource_effects.ReceiveProportional(
                {ResourceTypeEnum.food: 1},
                {ResourceTypeEnum.cow: 1})])

    def get_conditional_point(self, player: Player) -> PointEntity:
        if player is None:
            raise ValueError(str(player))
        return PointEntity(player.resources[ResourceTypeEnum.cow])


class StateParlorTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "State Parlor", 32,
            cost={ResourceTypeEnum.wood: 3, ResourceTypeEnum.coin: 5}, effects=[])

    def get_conditional_point(self, player: Player) -> PointEntity:
        if player is None:
            raise ValueError(str(player))

        adjacent_tile_locations = player.get_adjacent_tiles(self.location)
        adjacent_tiles = [
            player.get_tile_at_location(t)
            for t
            in map(
                lambda location_direction_pair: location_direction_pair[0],
                adjacent_tile_locations)]
        number_of_adjacent_dwellings = len([d for d in adjacent_tiles if d.is_dwelling])
        result = 4 * number_of_adjacent_dwellings
        return PointEntity(result)


class StoneStorageTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "Stone Storage", 36,
            cost={ResourceTypeEnum.wood: 3, ResourceTypeEnum.ore: 1})

    def get_conditional_point(self, player: Player) -> PointEntity:
        if player is None:
            raise ValueError(str(player))
        return PointEntity(player.resources[ResourceTypeEnum.stone])


class OreStorageTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "Ore Storage", 37,
            cost={ResourceTypeEnum.wood: 1, ResourceTypeEnum.ore: 2})

    def get_conditional_point(self, player: Player) -> PointEntity:
        if player is None:
            raise ValueError(str(player))
        return PointEntity(math.floor(player.resources[ResourceTypeEnum.ore] / 2))


class MainStorageTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "Main Storage", 39,
            cost={ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 1})

    def get_conditional_point(self, player: Player) -> PointEntity:
        if player is None:
            raise ValueError(str(player))
        return PointEntity(len([t for t in player.tiles if t.colour == TileColourEnum.Yellow]))


class WeaponStorageTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "Weapon Storage", 40,
            cost={ResourceTypeEnum.wood: 3, ResourceTypeEnum.stone: 2})

    def get_conditional_point(self, player: Player) -> PointEntity:
        if player is None:
            raise ValueError(str(player))
        return PointEntity(len([d for d in player.dwarves if d.has_weapon]))


class SuppliesStorageTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "Supplies Storage", 41,
            cost={ResourceTypeEnum.food: 3, ResourceTypeEnum.wood: 1})

    def get_conditional_point(self, player: Player) -> PointEntity:
        if player is None:
            raise ValueError(str(player))
        if all([d.has_weapon for d in player.dwarves]):
            result = 8
        else:
            result = 0
        return PointEntity(result)


class BroomChamberTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "Broom Chamber", 42,
            cost={ResourceTypeEnum.wood: 1})

    def get_conditional_point(self, player: Player) -> PointEntity:
        if player is None:
            raise ValueError(str(player))

        number_of_dwarfs = len(player.dwarves)
        if number_of_dwarfs == 5:
            return PointEntity(5)
        elif number_of_dwarfs == 6:
            return PointEntity(10)
        else:
            return PointEntity()


class TreasureChamberTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "Treasure Chamber", 43,
            cost={ResourceTypeEnum.wood: 1, ResourceTypeEnum.stone: 1})

    def get_conditional_point(self, player: Player) -> PointEntity:
        if player is None:
            raise ValueError(str(player))
        return PointEntity(player.resources[ResourceTypeEnum.ruby])


class FoodChamberTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "Food Chamber", 44,
            cost={ResourceTypeEnum.wood: 2, ResourceTypeEnum.vegetable: 2})

    def get_conditional_point(self, player: Player) -> PointEntity:
        if player is None:
            raise ValueError(str(player))

        result = min(player.resources[ResourceTypeEnum.veg], player.resources[ResourceTypeEnum.grain]) * 2
        return PointEntity(result)


class PrayerChamberTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "Prayer Chamber", 45,
            cost={ResourceTypeEnum.wood: 2})

    def get_conditional_point(self, player: Player) -> PointEntity:
        if player is None:
            raise ValueError(str(player))
        if any([d.has_weapon for d in player.dwarves]):
            result = 0
        else:
            result = 8
        return PointEntity(result)


class WritingChamberTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "Writing Chamber", 46,
            cost={ResourceTypeEnum.stone: 2})

    def get_conditional_point(self, player: Player) -> PointEntity:
        return PointEntity(0, 0, 7)


class FodderChamberTile(BaseConditionalPointTile):
    def __init__(self):
        BaseConditionalPointTile.__init__(
            self, "Fodder Chamber", 47,
            cost={ResourceTypeEnum.grain: 2, ResourceTypeEnum.stone: 1})

    def get_conditional_point(self, player: Player) -> PointEntity:
        if player is None:
            raise ValueError(str(player))
        default = FarmAnimalResourceTypeDefault()
        farm_animals: List[ResourceTypeEnum] = default.assign([])
        players_farm_animals: List[int] = [player.resources[x] for x in farm_animals]
        number_of_farm_animals: int = sum(players_farm_animals)
        result: int = math.floor(number_of_farm_animals / 3)

        return PointEntity(result)
