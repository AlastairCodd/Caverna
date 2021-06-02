from automated_tests.business_logic_tests.service_tests.processor_service_tests.twin_tile_placement_action_choice_processor_service_tests.given_a_twin_tile_placement_action_choice_processor_service import \
    Given_A_TwinTilePlacementActionChoiceProcessorService


class test_when_all_parameters_are_valid(Given_A_TwinTilePlacementActionChoiceProcessorService):
    def test_then_sut_should_not_be_none(self) -> None:
        self.assertIsNotNone(self.SUT)
