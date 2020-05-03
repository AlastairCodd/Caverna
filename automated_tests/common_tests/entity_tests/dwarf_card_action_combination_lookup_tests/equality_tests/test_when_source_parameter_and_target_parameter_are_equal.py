from automated_tests.common_tests.entity_tests.dwarf_card_action_combination_lookup_tests.given_a_dwarfCardActionCombinationLookup import \
    Given_A_DwarfCardActionCombinationLookup


class Test_When_source_parameter_and_target_parameter_are_equal(Given_A_DwarfCardActionCombinationLookup):
    def because(self) -> None:
        self._result: bool = self._validLookup == self._matchingValidLookup
        
    def test_then_result_should_be_true(self) -> None:
        self.assertTrue(self._result)
