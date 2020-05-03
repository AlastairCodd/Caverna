from typing import List, Tuple
from unittest.mock import Mock

from automated_tests.common_tests.entity_tests.dwarf_card_action_combination_lookup_tests.given_a_dwarfCardActionCombinationLookup import \
    Given_A_DwarfCardActionCombinationLookup
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.dwarf_card_action_combination_lookup import DwarfCardActionCombinationLookup
from core.baseClasses.base_card import BaseCard


class Test_When_(Given_A_DwarfCardActionCombinationLookup):
    def because(self) -> None:
        dwarf1: Dwarf = Mock(spec=Dwarf)
        dwarf2: Dwarf = Mock(spec=Dwarf)

        card1: BaseCard = Mock(spec=BaseCard)
        card2: BaseCard = Mock(spec=BaseCard)

        actions1: ActionChoiceLookup = Mock(spec=ActionChoiceLookup)
        actions2: ActionChoiceLookup = Mock(spec=ActionChoiceLookup)

        self._testCases: List[Tuple[str, DwarfCardActionCombinationLookup, DwarfCardActionCombinationLookup]] = [
            ("Test Dwarves",
             DwarfCardActionCombinationLookup(dwarf1, card1, actions1),
             DwarfCardActionCombinationLookup(dwarf2, card1, actions1)),
            ("Test Cards",
             DwarfCardActionCombinationLookup(dwarf1, card1, actions1),
             DwarfCardActionCombinationLookup(dwarf1, card2, actions1)),
            ("Test Actions",
             DwarfCardActionCombinationLookup(dwarf1, card1, actions1),
             DwarfCardActionCombinationLookup(dwarf1, card1, actions2)),
        ]
        
    def test_then_result_should_be_false(self) -> None:
        source: DwarfCardActionCombinationLookup
        target: DwarfCardActionCombinationLookup
        testLabel: str
        for testLabel, source, target in self._testCases:
            with self.subTest(label=testLabel):
                self.assertFalse(source == target)
