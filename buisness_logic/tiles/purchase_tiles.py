from buisness_logic.effects import purchase_effects, resource_effects
from core.constants import tile_ids
from core.enums.caverna_enums import ResourceTypeEnum
from core.baseClasses.base_tile import BaseTile
from common.entities import weapon


class CarpenterTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Carpenter", tile_ids.CarpenterTileId,
            cost={ResourceTypeEnum.stone: 1},
            effects=[purchase_effects.DecreasePrice(BaseTile, {ResourceTypeEnum.wood: 1})])


class StoneCarverTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Stone Carver", tile_ids.StoneCarverTileId,
            base_points=1,
            cost={ResourceTypeEnum.wood: 1},
            effects=[
                resource_effects.Receive({ResourceTypeEnum.stone: 2}),
                purchase_effects.DecreasePrice(BaseTile, {ResourceTypeEnum.stone: 1})])


class BlacksmithTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Blacksmith", tile_ids.BlacksmithTileId,
            base_points=3,
            cost={ResourceTypeEnum.wood: 1, ResourceTypeEnum.stone: 2},
            effects=[
                resource_effects.Receive({ResourceTypeEnum.ore: 2}),
                purchase_effects.DecreasePrice(weapon.Weapon, {ResourceTypeEnum.ore: 2})])


class BuilderTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Builder", tile_ids.BuilderTileId,
            base_points=2,
            cost={ResourceTypeEnum.stone: 1},
            effects=[
                purchase_effects.AllowSubstitutionForPurchase(
                    BaseTile,
                    substitute_for={ResourceTypeEnum.wood: 1},
                    substitute_with={ResourceTypeEnum.ore: 1}),
                purchase_effects.AllowSubstitutionForPurchase(
                    BaseTile,
                    substitute_for={ResourceTypeEnum.stone: 1},
                    substitute_with={ResourceTypeEnum.ore: 1})])
