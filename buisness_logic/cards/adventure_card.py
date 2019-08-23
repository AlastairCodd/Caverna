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
                giveDwarfAWeaponAction.GiveDwarfAWeaponAction(),
                Conditional(
                    ActionCombinationEnum.AndThen,
                    goOnAnExpeditionAction.GoOnAnExpeditionAction(1),
                    goOnAnExpeditionAction.GoOnAnExpeditionAction(1))))
