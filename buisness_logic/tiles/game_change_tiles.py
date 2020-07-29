from core.baseClasses.base_tile import BaseSpecificTile
from core.constants import tile_ids
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum
from buisness_logic.effects import *


class WorkRoomTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Work Room", tile_ids.WorkRoomTileId,
            base_points=2,
            cost={ResourceTypeEnum.stone: 1},
            effects=[board_effects.FurnishTunnelsEffect()])


class GuestRoomTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Guest Room", tile_ids.GuestRoomTileId,
            cost={ResourceTypeEnum.wood: 1, ResourceTypeEnum.stone: 1},
            effects=[action_effects.ChangeDecisionVerb(ActionCombinationEnum.EitherOr, ActionCombinationEnum.AndOr)])


class OfficeRoomTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Office Room", tile_ids.OfficeRoomTileId,
            cost={ResourceTypeEnum.stone: 1},
            effects=[board_effects.TwinTilesOverhangEffect()])
