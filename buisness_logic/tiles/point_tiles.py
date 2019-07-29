from typing import Dict, List
import math
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import TileTypeEnum, ResourceTypeEnum, TileColourEnum
from common.defaults.farm_animal_resource_type_default import FarmAnimalResourceTypeDefault
from buisness_logic.effects import *


class BaseConditionalPointTile(BaseTile):
    def invoke(self, source: Dict[TileTypeEnum, List[TileTypeEnum]]) -> Dict[TileTypeEnum, List[TileTypeEnum]]:
        raise NotImplementedError("base conditional point effect class")


class WeavingParlorTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "Weaving Parlor"
        self._id = 30
        self._isDwelling = False
        self._basePoints = 0
        self._cost = {ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 1}
        self._effect = [resource_effects.ReceiveProportional(
            {ResourceTypeEnum.sheep: 1},
            {ResourceTypeEnum.food: 1})]
        # when purchased receive 1 food per sheep
        self._conditionalPoints = lambda player: player.get_resources().get(ResourceTypeEnum.sheep, 0)
        # 1 per sheep


class MilkingParlorTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "Milking Parlor"
        self._id = 31
        self._isDwelling = False
        self._basePoints = 0
        self._cost = {ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 2}
        self._effect = [resource_effects.ReceiveProportional(
            {ResourceTypeEnum.cow: 1},
            {ResourceTypeEnum.food: 1})]
        # when purchased receive 1 food per cow
        self._conditionalPoints = lambda player: player.get_resources().get(ResourceTypeEnum.sheep, 0)
        # 1 per cow


class StateParlorTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "State Parlor"
        self._id = 32
        self._isDwelling = False
        self._basePoints = 0
        self._cost = {ResourceTypeEnum.wood: 3, ResourceTypeEnum.coin: 5}
        self._effect = []
        # when purchased per adjacent dwelling receive 2 food
        self._conditionalPoints = self._state_palour_points
        # 4 per adjacent dwelling

    def _state_palour_points(self, player) -> int:
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
        return result


class StoneStorageTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "Stone Storage"
        self._id = 36
        self._isDwelling = False
        self._basePoints = 0
        self._cost = {ResourceTypeEnum.wood: 3, ResourceTypeEnum.ore: 1}
        self._conditionalPoints = lambda player: player.get_resources().get(ResourceTypeEnum.stone, 0)
        # 1 per stone


class OreStorageTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "Ore Storage"
        self._id = 37
        self._isDwelling = False
        self._basePoints = 0
        self._cost = {ResourceTypeEnum.wood: 1, ResourceTypeEnum.ore: 2}
        self._conditionalPoints = lambda player: math.floor(player.get_resources().get(ResourceTypeEnum.ore, 0) / 2)
        # 1 per 2 ore


class MainStorageTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "Main Storage"
        self._id = 39
        self._isDwelling = False
        self._basePoints = 0
        self._cost = {ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 1}
        self._conditionalPoints = lambda player: len(
            [t for t in player.get_tiles() if t.colour == TileColourEnum.Yellow])
        # 2 per yellow furnishing


class WeaponStorageTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "Weapon Storage"
        self._id = 40
        self._isDwelling = False
        self._basePoints = 0
        self._cost = {ResourceTypeEnum.wood: 3, ResourceTypeEnum.stone: 2}
        self._conditionalPoints = lambda player: len([d for d in player.get_dwarves() if d.has_weapon()])
        # 3 per dwarf with weapon


class SuppliesStorageTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "Supplies Storage"
        self._id = 41
        self._isDwelling = False
        self._basePoints = 0
        self._cost = {ResourceTypeEnum.food: 3, ResourceTypeEnum.wood: 1}
        self._conditionalPoints = self._supplies_storage_points
        # 8 if all dwarves have a weapon

    def _supplies_storage_points(self, player) -> int:
        if player is None: raise ValueError(str(player))
        if all([d.has_weapon() for d in player.get_dwarves()]):
            result = 8
        else:
            result = 0
        return result


class BroomChamberTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "Broom Chamber"
        self._id = 42
        self._isDwelling = False
        self._basePoints = 0
        self._cost = {ResourceTypeEnum.wood: 1}
        self._conditionalPoints = self._broom_chamber_points
        # 5 for 5 dwarves and 5 for the 6th dwarf

    def _broom_chamber_points(self, player) -> int:
        if player is None: raise ValueError(str(player))

        numberOfDwarfs = len(player.get_dwarves())
        if numberOfDwarfs == 5:
            return 5
        elif numberOfDwarfs == 6:
            return 10
        else:
            return 0


class TreasureChamberTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "Treasure Chamber"
        self._id = 43
        self._isDwelling = False
        self._basePoints = 0
        self._cost = {ResourceTypeEnum.wood: 1, ResourceTypeEnum.stone: 1}
        self._effect = []
        self._conditionalPoints = lambda player: player.get_resources().get(ResourceTypeEnum.ruby, 0)
        # 1 per ruby


class FoodChamberTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "Food Chamber"
        self._id = 44
        self._isDwelling = False
        self._basePoints = 0
        self._cost = {ResourceTypeEnum.wood: 2, ResourceTypeEnum.vegetable: 2}
        self._effect = []
        self._conditionalPoints = self._food_chamber_points
        # 2 per vegetable and grain

    def _food_chamber_points(self, player) -> int:
        if player is None: raise ValueError(str(player))
        playerResources: Dict[ResourceTypeEnum, int] = player.get_resources()
        numberVeg = playerResources.get(ResourceTypeEnum.veg, 0)
        numberGrain = playerResources.get(ResourceTypeEnum.grain, 0)
        result = min(numberGrain, numberVeg) * 2
        return result


class PrayerChamberTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "Prayer Chamber"
        self._id = 45
        self._isDwelling = False
        self._basePoints = 0
        self._cost = {ResourceTypeEnum.wood: 2}
        self._effect = []
        self._conditionalPoints = self._prayer_chamber_points
        # 8 if no dwarves have a weapon

    def _prayer_chamber_points(self, player) -> int:
        if player is None: raise ValueError(str(player))
        if any([d.has_weapon() for d in player.get_dwarves()]):
            result = 0
        else:
            result = 8
        return result


class WritingChamberTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "Writing Chamber"
        self._id = 46
        self._isDwelling = False
        self._basePoints = 0
        self._cost = {ResourceTypeEnum.stone: 2}
        self._effect = []
        self._conditionalPoints = self._writing_chamber_points
        # prevents up to 7 negative points

    def _writing_chamber_points(self, player):
        if player is None: raise ValueError(str(player))
        raise NotImplementedError()


class FodderChamberTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "Fodder Chamber"
        self._id = 47
        self._isDwelling = False
        self._basePoints = 0
        self._cost = {ResourceTypeEnum.grain: 2, ResourceTypeEnum.stone: 1}
        self._effect = []
        self._conditionalPoints = self._fodder_chamber_points
        # 1 per 3 farm animals

    def _fodder_chamber_points(self, player) -> int:
        if player is None: raise ValueError(str(player))
        default = FarmAnimalResourceTypeDefault()
        farmAnimals: List[ResourceTypeEnum] = default.assign([])
        playersFarmAnimals = [player.get_resources().get(x, 0) for x in farmAnimals]
        numberOfFarmAnimals = playersFarmAnimals.count()
        result = math.floor(numberOfFarmAnimals / 3)
        return result
