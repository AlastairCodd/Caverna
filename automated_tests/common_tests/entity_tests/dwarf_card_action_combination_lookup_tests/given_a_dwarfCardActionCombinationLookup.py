from abc import ABC
from unittest import TestCase


# noinspection PyPep8Naming
from unittest.mock import Mock

from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.dwarf_card_action_combination_lookup import DwarfCardActionCombinationLookup
from core.baseClasses.base_card import BaseCard


class Given_A_DwarfCardActionCombinationLookup(TestCase, ABC):
    def setUp(self) -> None:
        dwarf: Dwarf = Mock(spec=Dwarf)
        card: BaseCard = Mock(spec=BaseCard)
        actions: ActionChoiceLookup = Mock(spec=ActionChoiceLookup)

        self._validLookup: DwarfCardActionCombinationLookup = DwarfCardActionCombinationLookup(dwarf, card, actions)
        self._matchingValidLookup: DwarfCardActionCombinationLookup = DwarfCardActionCombinationLookup(dwarf, card, actions)

        self.because()

    def because(self) -> None:
        pass
