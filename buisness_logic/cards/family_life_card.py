from buisness_logic.actions.get_a_baby_dwarf_action import GetABabyDwarfAction
from buisness_logic.actions.sowAction import SowAction
from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ActionCombinationEnum


class FamilyLifeCard(BaseCard):
    def __init__(self):
        BaseCard.__init__(
            self, "Family Life", 29, 3,
            Conditional(
                ActionCombinationEnum.AndOr,
                GetABabyDwarfAction(),
                SowAction()
            )
        )