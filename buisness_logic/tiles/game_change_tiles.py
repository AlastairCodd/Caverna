from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum
from buisness_logic.effects import *


class WorkRoomTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Work Room", 9,
            base_points=2,
            cost={ResourceTypeEnum.stone: 1},
            effects=[board_effects.FurnishTunnelsEffect()])


class GuestRoomTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Guest Room", 10,
            cost={ResourceTypeEnum.wood: 1, ResourceTypeEnum.stone: 1},
            effects=[action_effects.ChangeDecisionVerb(ActionCombinationEnum.EitherOr, ActionCombinationEnum.AndOr)])


class OfficeRoomTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Office Room", 11,
            cost={ResourceTypeEnum.stone: 1},
            effects=[board_effects.TwinTilesOverhangEffect()])
