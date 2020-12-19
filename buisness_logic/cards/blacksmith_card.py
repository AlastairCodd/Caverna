from buisness_logic.actions import *
from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ActionCombinationEnum


class BlacksmithCard(BaseCard):

    def __init__(self):
        BaseCard.__init__(
            self, "Blacksmith", 21, 1,
            actions=Conditional(
                ActionCombinationEnum.AndThenOr,
                give_dwarf_a_weapon_action.GiveDwarfAWeaponAction(),
                go_on_an_expedition_action.GoOnAnExpeditionAction(3)))
