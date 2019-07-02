class CuddleRoomTile(BaseTile):
	def __init__(self):
		self._name = "Cuddle Room"
		self._id = 6
		self._isDwelling = False
		self._basePoints = 2
		self._cost = { ResourceTypeEnum.wood: 1 }
		self._effect = [animalStorageEffects.StoreConditional( 
			{ ResourceTypeEnum.sheep: 1 },
			lambda p: len( p.GetDwarves() ) ) ]
			
class BreakfastRoomTile(BaseTile):
	def __init__(self):
		self._name = "Breakfast Room"
		self._id = 7
		self._isDwelling = False
		self._basePoints = 0
		self._cost = { ResourceTypeEnum.wood: 1 }
		self._effect = [animalStorageEffects.Store( { ResourceTypeEnum.cow: 3 } ) ]
		
			
class StubbleRoomTile(BaseTile):
	def __init__(self):
		self._name = "Stubble Room"
		self._id = 8
		self._isDwelling = False
		self._basePoints = 1
		self._cost = { ResourceTypeEnum.wood: 1, ResourceTypeEnum.ore: 1 }
		self._effect = [animalStorageEffects.ChangeAnimalStorageBase( { ResourceTypeEnum.cow: 3 } ) ]
		