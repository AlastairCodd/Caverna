from buisness_logic.actions.placeATileAction import PlaceATileAction
from buisness_logic.actions.receive_action import ReceiveAction
from buisness_logic.tiles.mine_tiles import RubyMineTile
from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ActionCombinationEnum, TileTypeEnum, ResourceTypeEnum


class RubyMineConstructionCard(BaseCard):
    def __init__(self):
        BaseCard.__init__(
            self, "Ruby Mine Construction", 25, 2,
            Conditional(
                ActionCombinationEnum.EitherOr,
                PlaceATileAction(
                    TileTypeEnum.rubyMine,
                    RubyMineTile,
                    override_requisite=[TileTypeEnum.tunnel]),
                Conditional(
                    ActionCombinationEnum.AndThen,
                    PlaceATileAction(
                        TileTypeEnum.rubyMine,
                        RubyMineTile,
                        override_requisite=[TileTypeEnum.deepTunnel]),
                    ReceiveAction({ResourceTypeEnum.ruby: 1})
                )
            )
        )