from typing import Dict

from automated_tests.business_logic_tests.service_tests.processor_service_tests.stable_placement_action_choice_processor_service_tests.given_a_stable_placement_action_choice_processor_service import \
    Given_A_StablePlacementActionChoiceProcessorService
from common.entities.placement_action_choice import PlacementActionChoice


class test_when_called(Given_A_StablePlacementActionChoiceProcessorService):
    def because(self) -> None:
        self._locations: Dict[int, int] = {
            0: 0,
            1: 1,
            2: 2,
            3: 3,

            4: 8,
            5: 9,
            6: 10,
            7: 11,

            8: 16,
            9: 17,
            10: 18,
            11: 19,

            12: 24,
            13: 25,
            14: 26,
            15: 27,

            16: 32,
            17: 33,
            18: 34,
            19: 35,

            20: 40,
            21: 41,
            22: 42,
            23: 43,
        }

    def test_then_result_should_be_expected(self) -> None:
        for index, location in self._locations.items():
            with self.subTest(position=index):
                calculated_location: PlacementActionChoice = self.SUT.convert_index_to_placement(index)
                self.assertEqual(location, calculated_location.location)
