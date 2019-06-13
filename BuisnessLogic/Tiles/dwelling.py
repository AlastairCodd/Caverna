from Core.cavernaEnums import ResourceTypeEnum
from BuisnessLogic.Effects import populationEffects, animalStorageEffect
from Core.baseTile import BaseTile

class Dwelling(BaseTile):
	def __init__(self):
		self._name = "Dwelling"
		self._id = 0
		self._isDwelling = True
		self._basePoints = 3
		self._cost = {
			ResourceTypeEnum.wood: 4,
			ResourceTypeEnum.stone: 3 }
		self._effect = [populationEffects.IncreasePopulationCapEffect( 1 )]
			
class SimpleStoneDwelling(BaseTile):
	def __init__(self):
		self._name = "Simple Dwelling (stone)"
		self._id = 1
		self._isDwelling = True
		self._basePoints = 0
		self._cost = {
			ResourceTypeEnum.wood: 4,
			ResourceTypeEnum.stone: 2 }
		self._effect = [populationEffects.IncreasePopulationCapEffect( 1 )]
			
class SimpleWoodDwelling(BaseTile):
	def __init__(self):
		self._name = "Simple Dwelling (wood)"
		self._id = 2
		self._isDwelling = True
		self._basePoints = 0
		self._cost = {
			ResourceTypeEnum.wood: 3,
			ResourceTypeEnum.stone: 3 }
		self._effect = [populationEffects.IncreasePopulationCapEffect( 1 )]
			
class MixedDwelling(BaseTile):
	def __init__(self):
		self._name = "Mixed Dwelling"
		self._id = 3
		self._isDwelling = True
		self._basePoints = 4
		self._cost = {
			ResourceTypeEnum.wood: 5,
			ResourceTypeEnum.stone: 4 }
		self._effect = [
			populationEffects.IncreasePopulationCapEffect( 1 ),
			animalStorageEffects.IncreasePopulationCapEffect( 1 )]
			
class CoupleDwelling(BaseTile):
	def __init__(self):
		self._name = "Couple Dwelling"
		self._id = 4
		self._isDwelling = True
		self._basePoints = 5
		self._cost = {
			ResourceTypeEnum.wood: 8,
			ResourceTypeEnum.stone: 6 }
		self._effect = [populationEffects.IncreasePopulationCapEffect( 2 )]
			
class AdditionalDwelling(BaseTile):
	def __init__(self):
		self._name = "Couple Dwelling"
		self._id = 5
		self._isDwelling = True
		self._basePoints = 5
		self._cost = {
			ResourceTypeEnum.wood: 4,
			ResourceTypeEnum.stone: 3 }
		self._effect = [populationEffects.AllowSixthDwarfEffect()]