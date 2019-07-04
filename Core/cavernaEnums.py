from enum import Enum, auto

class ResourceTypeEnum(Enum):
	stone = auto()
	wood = auto()
	ore = auto()
	ruby = auto()
	
	coin = auto()
	food = auto()
	
	grain = auto()
	veg = auto()
	
	sheep = auto()
	donkey = auto()
	cow = auto()
	boar = auto()
	dog = auto()
	
class TileTypeEnum(Enum):
	unavailable = auto()
	forest = auto()
	underground = auto()
	meadow = auto()
	field = auto()
	meadowFieldTwin = auto()
	cavern = auto()
	tunnel = auto()
	deepTunnel = auto()
	cavernTunnelTwin = auto()
	cavernCavernTwin = auto()
	pasture = auto()
	pastureTwin = auto()
	furnishedCavern = auto()
	furnishedDwelling = auto()
	oreMineDeepTunnelTwin = auto()
	rubyMine = auto()
	
class TileDimensionEnum(Enum):
	oneByOne = auto()
	twoByOne = auto()

class TileDirectionEnum(Enum):
	up = auto()
	right = auto()
	down = auto()
	left = auto()
	
class ActionCombinationEnum(Enum):
	EitherOr = auto()
	AndOr = auto()
	AndThenOr = auto()
	Or = auto()
	AndThen = auto()
	
class TriggerStateEnum(Enum):
	StartOfTurn = auto()
	OnPurchase = auto()
	UserChoice = auto()