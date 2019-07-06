from player import Player
from Core.baseEffect import BaseEffect

class BaseAnimalStorageEffect(BaseEffect):
	def Invoke(self, player: Player) -> bool:
		raise NotImplementedException("base population effect class")
	
class StoreAny(BaseAnimalStorageEffect):
	def __init__(self, quantity: int):
		self._quantity = quantity
    '''Add storage capactiy for some number of any type of animal'''

	def Invoke(self, player: Player) -> bool:
		raise NotImplementedException()
	
class StoreSpecific(BaseAnimalStorageEffect):
	def __init__(self, animals: Dict[ResourceTypeEnum]):
    '''Add storage capacity for some number of a specific type of animal
    
    Inputs: animals: a dictionary containing animals and the number which can be stored.
        This cannot be null.'''
        if animals is None: raise ValueError("animals")
		self._animals = animals

	def Invoke(self, player: Player) -> bool:
		raise NotImplementedException()
	
class StoreConditional(BaseAnimalStorageEffect):
	def __init__(self, then: Dict[ResourceTypeEnum], condition ):
    '''Add a conditional amount of storage capacity for a specific type of animal
    
    Inputs:
        then: the base unit of animals which can be stored, given the condition is met
            This cannot be null.
        condition: a function which works out how many units of animals can be stored. 
            This cannot be null.'''
		if condition is None: raise ValueError("Condition")
		if then is None: raise ValueError("then")
        self._condition = condition

	def Invoke(self, player: Player) -> bool:
        self._condition( player )
		raise NotImplementedException()
		
class ChangeAnimalStorageBase(BaseAnimalStorageEffect):
    '''Change where animals can be stored on base tiles
    
    Inputs:
        tiles: A list of tiles which can now have animals stored on them.
            This cannot be null.
        quantity: the quantity of animals which can be stored on this tile. 
            This overrides previous default values.
            This must be greater than or equal to 0.'''
    def __init__(self, tiles: List[ResourceTypeEnum], quantity: int):
        if tiles is None: raise ValueError("tiles")
        if quantity < 0: raise ValueError("quantity must be greater than zero")
    
	def Invoke(self, player: Player) -> bool:
		raise NotImplementedException()