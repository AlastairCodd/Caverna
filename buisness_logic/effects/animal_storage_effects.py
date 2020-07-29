from abc import abstractmethod, ABCMeta
from typing import Dict, List, Callable
from core.repositories.base_player_repository import BasePlayerRepository
from core.baseClasses.base_effect import BaseEffect
from core.enums.caverna_enums import ResourceTypeEnum, TileTypeEnum


class BaseAnimalStorageEffect(BaseEffect, metaclass=ABCMeta):
    def __init(self):
        self._farm_animals = [
            ResourceTypeEnum.sheep,
            ResourceTypeEnum.donkey,
            ResourceTypeEnum.boar,
            ResourceTypeEnum.cow]
        BaseEffect.__init__(self)

    @abstractmethod
    def get_animal_storage_buckets(
            self,
            player: BasePlayerRepository) -> List[Dict[ResourceTypeEnum, int]]:
        raise NotImplementedError("base population effect class")


class StoreAny(BaseAnimalStorageEffect):
    """Add storage capacity for some number of any type of animal"""

    def __init__(
            self,
            quantity: int):
        self._quantity: int = quantity
        BaseAnimalStorageEffect.__init__(self)

    def get_animal_storage_buckets(self, player: BasePlayerRepository) -> List[Dict[ResourceTypeEnum, int]]:
        result: List[Dict[ResourceTypeEnum, int]] = \
            [{farm_animal: self._quantity for farm_animal in self._farm_animals}]
        return result


class StoreSpecific(BaseAnimalStorageEffect):
    def  __init__(
            self,
            animals: Dict[ResourceTypeEnum, int]):
        """Add storage capacity for some number of a specific type of animal
    
        :param animals: A dictionary containing animals and the number which can be stored. This cannot be null. """
        if animals is None:
            raise ValueError("animals")
        self._animals = animals
        BaseAnimalStorageEffect.__init__(self)

    def get_animal_storage_buckets(self, player: BasePlayerRepository) -> List[Dict[ResourceTypeEnum, int]]:
        return [self._animals]


class StoreConditional(BaseAnimalStorageEffect):
    def __init__(self, animal_type: ResourceTypeEnum, condition: Callable[[BasePlayerRepository], int]):
        """Add a conditional amount of storage capacity for a specific type of animal
    
        Inputs:
            then: the base unit of animals which can be stored, given the condition is met
                This cannot be null.
            condition: a function which works out how many units of animals can be stored. 
                This cannot be null."""
        if condition is None:
            raise ValueError("Condition")
        self._animal_type = animal_type
        self._condition: Callable[[BasePlayerRepository], int] = condition
        BaseEffect.__init__(self)

    def get_animal_storage_buckets(self, player: BasePlayerRepository) -> List[Dict[ResourceTypeEnum, int]]:
        storage_multiplier: int = self._condition(player)
        result = [{farm_animal: storage_multiplier for farm_animal in self._farm_animals}]
        return result


class ChangeAnimalStorageBase(BaseAnimalStorageEffect):

    def __init__(self, tiles: List[TileTypeEnum], quantity: int):
        """Change where animals can be stored on base tiles
    
        :param tiles: A list of tiles which can now have animals stored on them. This cannot be null.
        :param quantity: the quantity of animals which can be stored on this tile.
                This overrides previous default values.
                This must be greater than or equal to 0."""
        if tiles is None:
            raise ValueError("tiles")
        if quantity < 0:
            raise ValueError("quantity must be greater than zero")
        BaseEffect.__init__(self)

    def get_animal_storage_buckets(self, player: BasePlayerRepository) -> bool:
        raise NotImplementedError()
