from automated_tests.business_logic_tests.action_tests.place_a_tile_action_tests.given_a_place_a_tile_action import Given_A_PlaceATileAction
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.result_lookup import ResultLookup


class test_when_effects_chosen_are_unavailable(Given_A_PlaceATileAction):
    def because(self) -> None:
        self.initialise_sut_as_tile_type_which_is_specific()

        self._result: ResultLookup[ActionChoiceLookup] = self.SUT.set_player_choice()

        self._action_invoked_result: ResultLookup[int] = self.SUT.invoke(
            self._player,
            None,               # Unused for this action
            self._dwarf_to_use  # Unused for this action
        )

    def test_then_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_true(self) -> None:
        self.assertTrue(self._result.flag)

    def test_then_result_value_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result.value)

    def test_then_result_value_should_be_expected(self) -> None:
        self.assertEqual(self._result.value, 1)

    def test_then_action_invoked_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._action_invoked_result)

    def test_then_action_invoked_result_flag_should_be_false(self) -> None:
        self.assertFalse(self._action_invoked_result.flag)

    def test_then_action_invoked_result_value_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._action_invoked_result.value)

    def test_then_action_invoked_result_value_should_be_expected(self) -> None:
        self.assertEqual(self._action_invoked_result.value, 0)
