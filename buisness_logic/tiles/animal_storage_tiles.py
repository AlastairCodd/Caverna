from core.baseClasses.base_tile import BaseTile
from core.constants import tile_ids
from core.enums.caverna_enums import ResourceTypeEnum
from buisness_logic.effects import *


class CuddleRoomTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Cuddle Room", tile_ids.CuddleRoomTileId,
            base_points=2,
            cost={ResourceTypeEnum.wood: 1},
            effects=[animal_storage_effects.StoreConditional(ResourceTypeEnum.sheep, lambda p: len(p.dwarves))])


class BreakfastRoomTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Breakfast Room", tile_ids.BreakfastRoomTileId,
            cost={ResourceTypeEnum.wood: 1},
            effects=[animal_storage_effects.Store({ResourceTypeEnum.cow: 3})])


class StubbleRoomTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Stubble Room", tile_ids.StubbleRoomTileId,
            base_points=1,
            cost={ResourceTypeEnum.wood: 1, ResourceTypeEnum.ore: 1},
            effects=[animal_storage_effects.ChangeAnimalStorageBase([ResourceTypeEnum.field], 1)])
