
class SlaughteringCaveTile(BaseTile):
	def __init__(self):
		self._name = "Slaughtering Cave"
		self._id = 24
		self._isDwelling = False
		self._basePoints = 2
		self._cost = { ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 2 }
		self._effect = [conversionEffect.ChangeFoodConversionRate( { 
			ResourceTypeEnum.donkey: 2,
			ResourceTypeEnum.sheep: 2,
			ResourceTypeEnum.boar: 3,
			ResourceTypeEnum.cow: 4,
			[ResourceTypeEnum.donkey, ResourceTypeEnum.donkey]: 4 } ) ]
			
class CookingCaveTile(BaseTile):
	def __init__(self):
		self._name = "Cooking Cave"
		self._id = 25
		self._isDwelling = False
		self._basePoints = 2
		self._cost = { ResourceTypeEnum.stone: 2 }
		self._effect = [conversionEffect.Convert( 
			{ ResourceTypeEnum.veg: 1, ResourceTypeEnum.grain: 1 }, 
			{ ResourceTypeEnum.food: 5 ) ]

class PeacefulCaveTile(BaseTile):
	def __init__(self):
		self._name = "Peaceful Cave"
		self._id = 29
		self._isDwelling = False
		self._basePoints = 2
		self._cost = { ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 1 }
		self._effect = [conversionEffect.ConvertConditional( 
			weapon.Weapon,
			lambda x: x.GetLevel()
	
	
#working cave
#mining cave
#breeding cave
#peaceful cave
