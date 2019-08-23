from typing import Dict, List
from common.entities.player import Player
from core.baseClasses.base_effect import BaseEffect
from core.enums.caverna_enums import ResourceTypeEnum


class BaseAnimalStorageEffect(BaseEffect):
    def invoke(self, player: Player) -> bool:
        raise NotImplementedError("base population effect class")


class StoreAny(BaseAnimalStorageEffect):
    """Add storage capacity for some number of any type of animal"""

    def __init__(self, quantity: int):
        self._quantity = quantity
        BaseEffect.__init__(self)

    def invoke(self, player: Player) -> bool:
        raise NotImplementedError()


class StoreSpecific(BaseAnimalStorageEffect):
    def __init__(self, animals: Dict[ResourceTypeEnum, int]):
        """Add storage capacity for some number of a specific type of animal
    
        Inputs: animals: a dictionary containing animals and the number which can be stored.
        This cannot be null. """
        if animals is None:
            raise ValueError("animals")
        self._animals = animals
        BaseEffect.__init__(self)

    def invoke(self, player: Player) -> bool:
        raise NotImplementedError()


class StoreConditional(BaseAnimalStorageEffect):
    def __init__(self, then: Dict[ResourceTypeEnum, int], condition):
        """Add a conditional amount of storage capacity for a specific type of animal
    
        Inputs:
            then: the base unit of animals which can be stored, given the condition is met
                This cannot be null.
            condition: a function which works out how many units of animals can be stored. 
                This cannot be null."""
        if condition is None:
            raise ValueError("Condition")
        if then is None:
            raise ValueError("then")
        self._condition = condition
        BaseEffect.__init__(self)

    def invoke(self, player: Player) -> bool:
        self._condition(player)
        raise NotImplementedError()


class ChangeAnimalStorageBase(BaseAnimalStorageEffect):

    def __init__(self, tiles: List[ResourceTypeEnum], quantity: int):
        """Change where animals can be stored on base tiles
    
        Inputs:
            tiles: A list of tiles which can now have animals stored on them.
                This cannot be null.
            quantity: the quantity of animals which can be stored on this tile. 
                This overrides previous default values.
                This must be greater than or equal to 0."""
        if tiles is None:
            raise ValueError("tiles")
        if quantity < 0:
            raise ValueError("quantity must be greater than zero")
        BaseEffect.__init__(self)

    def invoke(self, player: Player) -> bool:
        raise NotImplementedError()
