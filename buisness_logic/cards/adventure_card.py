from buisness_logic.actions import *
from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ActionCombinationEnum


class AdventureCard(BaseCard):

    def __init__(self):
        BaseCard.__init__(
            self, "Adventure", 31, 4,
            actions=Conditional(
                ActionCombinationEnum.AndThenOr,
                give_dwarf_a_weapon_action.GiveDwarfAWeaponAction(),
                Conditional(
                    ActionCombinationEnum.AndThen,
                    go_on_an_expedition_action.GoOnAnExpeditionAction(1),
                    go_on_an_expedition_action.GoOnAnExpeditionAction(1))))
