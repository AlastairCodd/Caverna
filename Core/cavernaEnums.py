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
	meadow = auto()
	field = auto()
	meadowFieldTwin = auto()
	cavern = auto()
	tunnel = auto()
	cavernTunnelTwin = auto()
	cavernCavernTwin = auto()
	pasture = auto()
	pastureTwin = auto()
	
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