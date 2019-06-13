from Core.cavernaEnums import ResourceTypeEnum
from BuisnessLogic.Effects import populationEffects, animalStorageEffect
from Core.baseTile import BaseTile

class CuddleRoomTile(BaseTile):
	def __init__(self):
		self._name = "Cuddle Room"
		self._id = 6
		self._isDwelling = False
		self._basePoints = 2
		self._cost = { ResourceTypeEnum.wood: 1 }
		self._effect = [animalStorageEffect.ConditionalStorageEffect( Per, ResourceTypeEnum.sheep, dwarves )]
			
class BreakfastRoomTile(BaseTile):
	def __init__(self):
		self._name = "Breakfast Room"
		self._id = 7
		self._isDwelling = False
		self._basePoints = 0
		self._cost = { ResourceTypeEnum.wood: 1 }
		self._effect = [animalStorageEffect.IncreasePopulationCapEffect( 3, ResourceTypeEnum.cow )]
			
class StubbleRoomTile(BaseTile):
	def __init__(self):
		self._name = "Stubble Room"
		self._id = 8
		self._isDwelling = False
		self._basePoints = 1
		self._cost = {
			ResourceTypeEnum.wood: 1,
			ResourceTypeEnum.ore: 1 }
		self._effect = [animalStorageEffect.IncreasePopulationCapForTileTypeEffect( 1, TileTypeEnum.field )]
			
class WorkRoomTile(BaseTile):
	def __init__(self):
		self._name = "Work Room"
		self._id = 9
		self._isDwelling = False
		self._basePoints = 2
		self._cost = { ResourceTypeEnum.stone: 1 }
		self._effect = [boardEffects.FurnishTunnelsEffect()]
			
class GuestRoomTile(BaseTile):
	def __init__(self):
		self._name = "Guest Room"
		self._id = 10
		self._isDwelling = False
		self._basePoints = 0
		self._cost = {
			ResourceTypeEnum.wood: 1,
			ResourceTypeEnum.stone: 1 }
		self._effect = [actionEffects.ChangeDecisionVerb( ActionCombinationEnum.EitherOr, ActionCombinationEnum.AndOr )]
			
class OfficeRoomTile(BaseTile):
	def __init__(self):
		self._name = "Office Room"
		self._id = 11
		self._basePoints = 0
		self._isDwelling = True
		self._cost = { ResourceTypeEnum.stone: 1 }
		self._effect = [boardEffects.TwinTilesOverhangEffect()]