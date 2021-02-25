from abc import abstractmethod, ABCMeta
from typing import Dict, List, Callable

from common.entities.result_lookup import ResultLookup
from common.entities.tile_entity import TileEntity
from core.constants import resource_types
from core.repositories.base_player_repository import BasePlayerRepository
from core.baseClasses.base_effect import BaseEffect
from core.enums.caverna_enums import ResourceTypeEnum, TileTypeEnum


class BaseAnimalStorageEffect(BaseEffect, metaclass=ABCMeta):
    @abstractmethod
    def get_animal_storage_buckets(
            self,
            player: BasePlayerRepository) -> Dict[ResourceTypeEnum, int]:
        raise NotImplementedError("base population effect class")


class StoreAnyAnimalEffect(BaseAnimalStorageEffect):
    def __init__(
            self,
            quantity: int):
        """Add storage capacity for some number of any type of animal"""
        self._quantity: int = quantity

    def get_animal_storage_buckets(
            self,
            player: BasePlayerRepository) -> Dict[ResourceTypeEnum, int]:
        if player is None:
            raise ValueError("Player")
        result: Dict[ResourceTypeEnum, int] = {farm_animal: self._quantity for farm_animal in resource_types.farm_animals}
        return result


class StoreSpecificAnimalEffect(BaseAnimalStorageEffect):
    def __init__(
            self,
            space_for_animals: Dict[ResourceTypeEnum, int]):
        """Add storage capacity for some number of a specific type of animal
        :param space_for_animals: A dictionary of animals and the number which can be stored. This cannot be null. """
        if space_for_animals is None:
            raise ValueError("animals")
        self._animal_storage_buckets: Dict[ResourceTypeEnum, int] = space_for_animals

    def get_animal_storage_buckets(
            self,
            player: BasePlayerRepository) -> Dict[ResourceTypeEnum, int]:
        return self._animal_storage_buckets.copy()


class StoreConditionalAnimalEffect(BaseAnimalStorageEffect):
    def __init__(
            self,
            animal_type: ResourceTypeEnum,
            condition: Callable[[BasePlayerRepository], int]):
        """Add a conditional amount of storage capacity for a specific type of animal
    
        :param animal_type: The animal which may be stored as many times as the condition is met.
        :param condition: A function which returns the number of animals which can be stored. This cannot be null."""
        if condition is None:
            raise ValueError("Condition cannot be None")
        if animal_type not in resource_types.farm_animals:
            raise ValueError(f"Cannot store {animal_type} in an animal storage effect")
        self._animal_type: ResourceTypeEnum = animal_type
        self._condition: Callable[[BasePlayerRepository], int] = condition
        BaseEffect.__init__(self)

    def get_animal_storage_buckets(
            self,
            player: BasePlayerRepository) -> Dict[ResourceTypeEnum, int]:
        if player is None:
            raise ValueError("Player cannot be None")
        storage_multiplier: int = self._condition(player)
        result: Dict[ResourceTypeEnum, int] = {self._animal_type: storage_multiplier}
        return result


class ChangeAnimalStorageBaseEffect(BaseEffect):
    def __init__(
            self,
            tiles: List[TileTypeEnum],
            animals_which_can_be_stored: Dict[ResourceTypeEnum, int],
            condition: Callable[[BasePlayerRepository, TileEntity], int]):
        """Change where animals can be stored on base tiles
    
        :param tiles: A list of tiles which can now have animals stored on them. This cannot be null.
        :param animals_which_can_be_stored: The animals which may be stored, scaled by as many times as the condition is met.
        :param condition: A function which returns the number of animals which can be stored. This cannot be null."""
        if tiles is None or len(tiles) == 0:
            raise ValueError("Tile effected by change in base type may not be None or empty")
        if condition is None:
            raise ValueError("Condition may not be None")
        for animal_type in animals_which_can_be_stored:
            if animal_type not in [ResourceTypeEnum.sheep, ResourceTypeEnum.donkey, ResourceTypeEnum.boar, ResourceTypeEnum.cow]:
                raise ValueError(f"Cannot store {animal_type} in an animal storage effect")

        self._tiles: List[TileTypeEnum] = tiles
        self._animals_which_can_be_stored: Dict[ResourceTypeEnum, int] = animals_which_can_be_stored
        self._condition: Callable[[BasePlayerRepository, TileEntity], int] = condition

    def get_animal_storage_buckets_for_tile(
            self,
            player: BasePlayerRepository,
            tile: TileEntity) -> ResultLookup[Dict[ResourceTypeEnum, int]]:
        if player is None:
            raise ValueError("Player cannot be None")
        if tile is None:
            raise ValueError("Tile cannot be None")
        result: ResultLookup[Dict[ResourceTypeEnum, int]]
        if tile.tile_type in self._tiles:
            storage_multiplier: int = self._condition(player, tile)
            bucket: Dict[ResourceTypeEnum, int] = {
                animal_type: self._animals_which_can_be_stored[animal_type] * storage_multiplier
                for animal_type
                in self._animals_which_can_be_stored}
            result = ResultLookup(True, bucket)
        else:
            result = ResultLookup(False, {}, errors="Tile is not of type under influence of effect.")
        return result

