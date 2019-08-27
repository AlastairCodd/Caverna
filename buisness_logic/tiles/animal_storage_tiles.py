from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum
from buisness_logic.effects import *


class CuddleRoomTile(BaseTile):
    def __init__(self):
        super().__init__(
            "Cuddle Room", 6, False, 2,
            {ResourceTypeEnum.wood: 1},
            [animal_storage_effects.StoreConditional(
                ResourceTypeEnum.sheep,
                lambda p: len(p.dwarves))])


class BreakfastRoomTile(BaseTile):
    def __init__(self):
        super().__init__(
            "Breakfast Room", 7, False, 0,
            {ResourceTypeEnum.wood: 1},
            [animal_storage_effects.Store({ResourceTypeEnum.cow: 3})])


class StubbleRoomTile(BaseTile):
    def __init__(self):
        super().__init__(
            "Stubble Room", 8, False, 1,
            {ResourceTypeEnum.wood: 1, ResourceTypeEnum.ore: 1},
            [animal_storage_effects.ChangeAnimalStorageBase([ResourceTypeEnum.field], 1)])
