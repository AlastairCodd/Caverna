from automated_tests.common_tests.entity_tests.dwarf_card_action_combination_lookup_tests.given_a_dwarfCardActionCombinationLookup import \
    Given_A_DwarfCardActionCombinationLookup


class Test_When_Target_Is_Null(Given_A_DwarfCardActionCombinationLookup):
    def because(self) -> None:
        self._result: bool = self._validLookup == None

    def test_then_result_should_be_false(self) -> None:
        self.assertFalse(self._result)

