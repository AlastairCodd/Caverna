from core.enums.caverna_enums import TileTypeEnum, ResourceTypeEnum
from core.baseClasses.base_tile import BaseTile


class TileEntity(object):
    def __init__(
            self,
            tile_id: int,
            tile_type: TileTypeEnum,
            base_tile: BaseTile = None,
            animal_type: ResourceTypeEnum = None,
            animal_quantity: int = 0,
            has_stable: bool = False):
        self._id = tile_id
        self._tileType = tile_type
        self._baseTile = base_tile
        self._animalType = animal_type
        self._animalQuantity = animal_quantity
        self._hasStable = has_stable

    @property
    def tile(self):
        return self._baseTile

    def set_tile(self, base_tile: BaseTile):
        if self._baseTile is not None:
            raise ValueError("Cannot set base tile; tile entity already has a tile")
        self._baseTile = base_tile

    def get_tile_type(self) -> TileTypeEnum:
        return self._tileType
