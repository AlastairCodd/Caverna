from buisness_logic.effects import purchase_effects, resource_effects
from core.constants import tile_ids
from core.enums.caverna_enums import ResourceTypeEnum
from core.baseClasses.base_tile import BaseSpecificTile


class CarpenterTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Carpenter", tile_ids.CarpenterTileId,
            cost={ResourceTypeEnum.stone: 1},
            effects=[purchase_effects.DecreasePriceOfTileEffect({ResourceTypeEnum.wood: 1})])


class StoneCarverTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Stone Carver", tile_ids.StoneCarverTileId,
            base_points=1,
            cost={ResourceTypeEnum.wood: 1},
            effects=[
                resource_effects.ReceiveOnPurchaseEffect({ResourceTypeEnum.stone: 2}),
                purchase_effects.DecreasePriceOfTileEffect({ResourceTypeEnum.stone: 1})])


class BlacksmithTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Blacksmith", tile_ids.BlacksmithTileId,
            base_points=3,
            cost={ResourceTypeEnum.wood: 1, ResourceTypeEnum.stone: 2},
            effects=[
                resource_effects.ReceiveOnPurchaseEffect({ResourceTypeEnum.ore: 2}),
                purchase_effects.DecreasePriceOfWeapon({ResourceTypeEnum.ore: 2})])


class BuilderTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Builder", tile_ids.BuilderTileId,
            base_points=2,
            cost={ResourceTypeEnum.stone: 1},
            effects=[
                purchase_effects.AllowSubstitutionForPurchaseEffect(
                    substitute_for={ResourceTypeEnum.wood: 1},
                    substitute_with={ResourceTypeEnum.ore: 1}),
                purchase_effects.AllowSubstitutionForPurchaseEffect(
                    substitute_for={ResourceTypeEnum.stone: 1},
                    substitute_with={ResourceTypeEnum.ore: 1})])
