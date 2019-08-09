from abc import ABC, abstractmethod
from typing import Dict, List, Callable
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

        super().__init__(name, tile_id, is_dwelling, base_points, cost, effects, TileColourEnum.Yellow)

    @abstractmethod
    def get_conditional_point(self, player: Player) -> PointEntity:
        pass


class WeavingParlorTile(BaseConditionalPointTile):
    def __init__(self):
        super().__init__("Weaving Parlor", 30, cost={ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 1},
                         effects=[resource_effects.ReceiveProportional(
                             input={ResourceTypeEnum.food: 1},
                             proportionalTo={ResourceTypeEnum.sheep: 1})])

    def get_conditional_point(self, player: Player) -> PointEntity:
        if player is None:
            raise ValueError(str(player))
        return PointEntity(player.resources[ResourceTypeEnum.sheep])


class MilkingParlorTile(BaseConditionalPointTile):
    def __init__(self):
        super().__init__("Milking Parlor", 31, cost={ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 2},
                         effects=[resource_effects.ReceiveProportional(
                             {ResourceTypeEnum.food: 1},
                             {ResourceTypeEnum.cow: 1})])

    def get_conditional_point(self, player: Player) -> PointEntity:
        if player is None:
            raise ValueError(str(player))
        return PointEntity(player.resources[ResourceTypeEnum.cow])


class StateParlorTile(BaseConditionalPointTile):
    def __init__(self):
        super().__init__("State Parlor", 32, cost={ResourceTypeEnum.wood: 3, ResourceTypeEnum.coin: 5}, effects=[])

    def get_conditional_point(self, player: Player) -> PointEntity:
        if player is None:
            raise ValueError(str(player))

        adjacentTileLocations = player.get_adjacent_tiles(self.location)
        adjacentTiles = [
            player.get_tile_at_location(t)
            for t
            in map(
                lambda locationDirectionPair: locationDirectionPair[0],
                adjacentTileLocations)]
        numberOfAdjacentDwellings = len([d for d in adjacentTiles if d.is_dwelling])
        result = 4 * numberOfAdjacentDwellings
        return PointEntity(result)


class StoneStorageTile(BaseConditionalPointTile):
    def __init__(self):
        super().__init__("Stone Storage", 36, cost={ResourceTypeEnum.wood: 3, ResourceTypeEnum.ore: 1})

    def get_conditional_point(self, player: Player) -> PointEntity:
        if player is None:
            raise ValueError(str(player))
        return PointEntity(player.resources[ResourceTypeEnum.stone])


class OreStorageTile(BaseConditionalPointTile):
    def __init__(self):
        super().__init__("Ore Storage", 37, cost={ResourceTypeEnum.wood: 1, ResourceTypeEnum.ore: 2})

    def get_conditional_point(self, player: Player) -> PointEntity:
        if player is None:
            raise ValueError(str(player))
        return PointEntity(math.floor(player.resources[ResourceTypeEnum.ore] / 2))


class MainStorageTile(BaseConditionalPointTile):
    def __init__(self):
        super().__init__("Main Storage", 39, cost={ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 1})

    def get_conditional_point(self, player: Player) -> PointEntity:
        if player is None:
            raise ValueError(str(player))
        return PointEntity(len( [t for t in player.get_tiles() if t.colour == TileColourEnum.Yellow]))


class WeaponStorageTile(BaseConditionalPointTile):
    def __init__(self):
        super().__init__("Weapon Storage", 40, cost={ResourceTypeEnum.wood: 3, ResourceTypeEnum.stone: 2})

    def get_conditional_point(self, player: Player) -> PointEntity:
        if player is None:
            raise ValueError(str(player))
        return PointEntity(len([d for d in player.dwarves if d.has_weapon]))


class SuppliesStorageTile(BaseConditionalPointTile):
    def __init__(self):
        super().__init__("Supplies Storage", 41, cost={ResourceTypeEnum.food: 3, ResourceTypeEnum.wood: 1})

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
        super().__init__("Broom Chamber", 42, cost={ResourceTypeEnum.wood: 1})

    def get_conditional_point(self, player: Player) -> PointEntity:
        if player is None:
            raise ValueError(str(player))

        numberOfDwarfs = len(player.dwarves)
        if numberOfDwarfs == 5:
            return PointEntity(5)
        elif numberOfDwarfs == 6:
            return PointEntity(10)
        else:
            return PointEntity()


class TreasureChamberTile(BaseConditionalPointTile):
    def __init__(self):
        super().__init__("Treasure Chamber", 43, cost={ResourceTypeEnum.wood: 1, ResourceTypeEnum.stone: 1})

    def get_conditional_point(self, player: Player) -> PointEntity:
        if player is None:
            raise ValueError(str(player))
        return PointEntity(player.resources[ResourceTypeEnum.ruby])


class FoodChamberTile(BaseConditionalPointTile):
    def __init__(self):
        super().__init__("Food Chamber", 44, cost={ResourceTypeEnum.wood: 2, ResourceTypeEnum.vegetable: 2})

    def get_conditional_point(self, player: Player) -> PointEntity:
        if player is None:
            raise ValueError(str(player))

        result = min(player.resources[ResourceTypeEnum.veg], player.resources[ResourceTypeEnum.grain]) * 2
        return PointEntity(result)


class PrayerChamberTile(BaseConditionalPointTile):
    def __init__(self):
        super().__init__("Prayer Chamber", 45, cost={ResourceTypeEnum.wood: 2})

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
        super(WritingChamberTile, self).__init__("Writing Chamber", 46, cost={ResourceTypeEnum.stone: 2})

    def get_conditional_point(self, player: Player) -> PointEntity:
        return PointEntity(0, 0, 7)


class FodderChamberTile(BaseConditionalPointTile):
    def __init__(self):
        super().__init__("Fodder Chamber", 47, cost={ResourceTypeEnum.grain: 2, ResourceTypeEnum.stone: 1})

    def get_conditional_point(self, player: Player) -> PointEntity:
        if player is None: raise ValueError(str(player))
        default = FarmAnimalResourceTypeDefault()
        farmAnimals: List[ResourceTypeEnum] = default.assign([])
        playersFarmAnimals: List[int] = [player.resources[x] for x in farmAnimals]
        numberOfFarmAnimals: int = sum(playersFarmAnimals)
        result: int = math.floor(numberOfFarmAnimals / 3)

        return PointEntity(result)
