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

    begging_marker = auto()


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
    oreMine = auto()
    oreMineDeepTunnelTwin = auto()
    rubyMine = auto()


class TileDimensionEnum(Enum):
    oneByOne = auto()
    twoByOne = auto()


class TileDirectionEnum(Enum):
    up = 0
    right = 1
    down = 2
    left = 3


class ActionCombinationEnum(Enum):
    EitherOr = auto()
    AndOr = auto()
    And = auto()
    AndThenOr = auto()
    OrAndThenStrict = auto()
    Or = auto()
    AndThen = auto()


class TileColourEnum(Enum):
    Brown = auto()
    Green = auto()
    Yellow = auto()
