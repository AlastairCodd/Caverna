from typing import Dict, List, Callable
import math

from common.entities.point_entity import PointEntity
from core.baseClasses.base_effect import BaseEffect
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum, TileColourEnum
from common.entities.player import Player
from common.defaults.farm_animal_resource_type_default import FarmAnimalResourceTypeDefault
from buisness_logic.effects import *


class BaseConditionalPointTile(BaseTile):
    def __init__(
            self,
            name: str,
            tile_id: int,
            is_dwelling: bool = False,
            base_points: int = 0,
            cost: Dict[ResourceTypeEnum, int] = {},
            effects: List[BaseEffect] = [],
            conditional_points: Callable[[Player], PointEntity] = None):
        self._conditional_points = conditional_points
        super().__init__(
            name,
            tile_id,
            is_dwelling,
            base_points,
            cost,
            effects)

    def get_conditional_point(self, player: Player) -> PointEntity:
        return self._conditional_points(player)

class WeavingParlorTile(BaseConditionalPointTile):
    def __init__(self):
        super().__init__(
            "Weaving Parlor", 30,
            cost={ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 1},
            # when purchased receive 1 food per sheep
            effects=[resource_effects.ReceiveProportional(
                input={ResourceTypeEnum.food: 1},
                proportionalTo={ResourceTypeEnum.sheep: 1})],
            # 1 per sheep
            conditional_points=lambda player: PointEntity(player.get_resources().get(ResourceTypeEnum.sheep, 0)))


class MilkingParlorTile(BaseConditionalPointTile):
    def __init__(self):
        super().__init__(
            "Milking Parlor", 31,
            cost={ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 2},
            # when purchased receive 1 food per cow
            effects=[resource_effects.ReceiveProportional(
                {ResourceTypeEnum.food: 1},
                {ResourceTypeEnum.cow: 1})],
            # 1 per cow
            conditional_points=lambda player: PointEntity(player.get_resources().get(ResourceTypeEnum.sheep, 0)))


class StateParlorTile(BaseConditionalPointTile):
    def __init__(self):
        super().__init__(
            "State Parlor", 32,
            cost={ResourceTypeEnum.wood: 3, ResourceTypeEnum.coin: 5},
            # when purchased per adjacent dwelling receive 2 food
            effects=[],
            # 4 per adjacent dwelling
            conditional_points=self._state_palour_points)

    def _state_palour_points(self, player) -> PointEntity:
        if player is None: raise ValueError(str(player))

        adjacentTileLocations = player.get_adjacent_tiles()
        adjacentTiles = [
            player.get_tile_at_location(t)
            for t
            in map(
                lambda locationDirectionPair: locationDirectionPair[0],
                adjacentTileLocations)]
        numberOfAdjacentDwellings = len([d for d in adjacentTiles if d.is_dwelling()])
        result = 4 * numberOfAdjacentDwellings
        return PointEntity(result)


class StoneStorageTile(BaseConditionalPointTile):
    def __init__(self):
        super().__init__(
            "Stone Storage", 36,
            cost={ResourceTypeEnum.wood: 3, ResourceTypeEnum.ore: 1},
            # 1 per stone
            conditional_points=lambda player: PointEntity(player.get_resources().get(ResourceTypeEnum.stone, 0)))


class OreStorageTile(BaseConditionalPointTile):
    def __init__(self):
        super().__init__(
            "Ore Storage", 37,
            cost={ResourceTypeEnum.wood: 1, ResourceTypeEnum.ore: 2},
            # 1 per 2 ore
            conditional_points=lambda player: PointEntity(
                math.floor(player.get_resources().get(ResourceTypeEnum.ore, 0) / 2)))


class MainStorageTile(BaseConditionalPointTile):
    def __init__(self):
        super().__init__(
            "Main Storage", 39,
            cost={ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 1},
            # 2 per yellow furnishing
            conditional_points=lambda player: PointEntity(len(
                [t for t in player.get_tiles() if t.colour == TileColourEnum.Yellow])))


class WeaponStorageTile(BaseConditionalPointTile):
    def __init__(self):
        super().__init__(
            "Weapon Storage", 40,
            cost={ResourceTypeEnum.wood: 3, ResourceTypeEnum.stone: 2},
            # 3 per dwarf with weapon
            conditional_points=lambda player: PointEntity(len([d for d in player.get_dwarves() if d.has_weapon()])))


class SuppliesStorageTile(BaseConditionalPointTile):
    def __init__(self):
        super().__init__(
            "Supplies Storage", 41, cost={ResourceTypeEnum.food: 3, ResourceTypeEnum.wood: 1},
            # 8 if all dwarves have a weapon
            conditional_points=self._supplies_storage_points)

    def _supplies_storage_points(self, player) -> PointEntity:
        if player is None: raise ValueError(str(player))
        if all([d.has_weapon() for d in player.get_dwarves()]):
            result = 8
        else:
            result = 0
        return PointEntity(result)


class BroomChamberTile(BaseConditionalPointTile):
    def __init__(self):
        super().__init__(
            "Broom Chamber", 42,
            cost={ResourceTypeEnum.wood: 1},
            # 5 for 5 dwarves and 5 for the 6th dwarf
            conditional_points=self._broom_chamber_points)

    def _broom_chamber_points(self, player) -> PointEntity:
        if player is None: raise ValueError(str(player))

        numberOfDwarfs = len(player.get_dwarves())
        if numberOfDwarfs == 5:
            return PointEntity(5)
        elif numberOfDwarfs == 6:
            return PointEntity(10)
        else:
            return PointEntity()


class TreasureChamberTile(BaseConditionalPointTile):
    def __init__(self):
        super().__init__(
            "Treasure Chamber", 43,
            cost={ResourceTypeEnum.wood: 1, ResourceTypeEnum.stone: 1},
            # 1 per ruby
            conditional_points=lambda player: player.get_resources().get(ResourceTypeEnum.ruby, 0))


class FoodChamberTile(BaseConditionalPointTile):
    def __init__(self):
        super().__init__(
            "Food Chamber", 44,
            cost={ResourceTypeEnum.wood: 2, ResourceTypeEnum.vegetable: 2},
            # 2 per vegetable and grain
            conditional_points=self._food_chamber_points)

    def _food_chamber_points(self, player) -> PointEntity:
        if player is None: raise ValueError(str(player))
        playerResources: Dict[ResourceTypeEnum, int] = player.get_resources()
        numberVeg = playerResources.get(ResourceTypeEnum.veg, 0)
        numberGrain = playerResources.get(ResourceTypeEnum.grain, 0)
        result = min(numberGrain, numberVeg) * 2
        return PointEntity(result)


class PrayerChamberTile(BaseConditionalPointTile):
    def __init__(self):
        super().__init__(
            "Prayer Chamber", 45,
            cost={ResourceTypeEnum.wood: 2},
            # 8 if no dwarves have a weapon
            conditional_points=self._prayer_chamber_points)

    def _prayer_chamber_points(self, player) -> PointEntity:
        if player is None: raise ValueError(str(player))
        if any([d.has_weapon() for d in player.get_dwarves()]):
            result = 0
        else:
            result = 8
        return PointEntity(result)


class WritingChamberTile(BaseConditionalPointTile):
    def __init__(self):
        super(WritingChamberTile, self).__init__(
            "Writing Chamber", 46,
            cost={ResourceTypeEnum.stone: 2},
            # prevents up to 7 negative points
            conditional_points=self._writing_chamber_points)

    def _writing_chamber_points(self, player):
        return PointEntity(0, 0, 7)


class FodderChamberTile(BaseConditionalPointTile):
    def __init__(self):
        super().__init__(
            "Fodder Chamber", 47,
            cost={ResourceTypeEnum.grain: 2, ResourceTypeEnum.stone: 1},
            # 1 per 3 farm animals
            conditional_points=self._fodder_chamber_points)

    def _fodder_chamber_points(self, player) -> PointEntity:
        if player is None: raise ValueError(str(player))
        default = FarmAnimalResourceTypeDefault()
        farmAnimals: List[ResourceTypeEnum] = default.assign([])
        playersFarmAnimals: List[int] = [player.get_resources().get(x, 0) for x in farmAnimals]
        numberOfFarmAnimals: int = sum(playersFarmAnimals)
        result: int = math.floor(numberOfFarmAnimals / 3)

        return PointEntity(result)
