from buisness_logic.actions.get_a_baby_dwarf_action import GetABabyDwarfAction
from buisness_logic.actions.sow_action import SowAction
from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.constants import card_ids
from core.enums.caverna_enums import ActionCombinationEnum


class FamilyLifeCard(BaseCard):
    def __init__(self):
        BaseCard.__init__(
            self, "Family Life", card_ids.FamilyLifeCardId, 3,
            Conditional(
                ActionCombinationEnum.AndOr,
                GetABabyDwarfAction(),
                SowAction()
            )
        )