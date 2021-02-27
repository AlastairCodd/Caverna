from buisness_logic.actions import *
from buisness_logic.tiles.mine_tiles import RubyMineTile
from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.constants import card_ids
from core.enums.caverna_enums import ActionCombinationEnum, TileTypeEnum, ResourceTypeEnum


class RubyMineConstructionCard(BaseCard):
    def __init__(self):
        BaseCard.__init__(
            self, "Ruby Mine Construction", card_ids.RubyMineConstructionCardId, 2,
            Conditional(
                ActionCombinationEnum.EitherOr,
                place_a_single_tile_action.PlaceASingleTileAction(
                    TileTypeEnum.rubyMine,
                    RubyMineTile,
                    override_requisite=[TileTypeEnum.tunnel]),
                Conditional(
                    ActionCombinationEnum.AndThen,
                    place_a_single_tile_action.PlaceASingleTileAction(
                        TileTypeEnum.rubyMine,
                        RubyMineTile,
                        override_requisite=[TileTypeEnum.deepTunnel]),
                    receive_action.ReceiveAction({ResourceTypeEnum.ruby: 1})
                )
            )
        )