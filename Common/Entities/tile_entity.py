from Core.cavernaEnums import TileTypeEnum, ResourceTypeEnum
from Core.baseTile import BaseTile

class TileEntity(object):
    def __init__(
        self,
        id: int,
        tileType: TileTypeEnum,
        baseTile: BaseTile = None,
        animalType: ResourceTypeEnum = None,
        animalQuantity: int = 0,
        hasStable: bool = False ):
        self._id = id
        self._tileType = tileType
        self._baseTile = baseTile
        self._animalType = animalType
        self._animalQuantity = animalQuantity
        self._hasStable = hasStable

    def get_tile(self):
        return self._baseTile