from typing import List

from automated_tests.business_logic_tests.service_tests.processor_service_tests.animals_to_breed_processor_service_tests.given_an_animals_to_breed_action_choice_processor_service import \
    Given_A_AnimalsToBreedActionChoiceProcessorService
from buisness_logic.services.processor_services.animals_to_breed_action_choice_processor_service import AnimalsToBreedActionChoice
from core.enums.caverna_enums import ResourceTypeEnum


class test_when_number_above_threshold_is_less_than_maximum(Given_A_AnimalsToBreedActionChoiceProcessorService):
    def because(self) -> None:
        self.SUT.offset = 0

        action_choice: List[float] = [0.1 for _ in range(self.SUT.length)]
        action_choice[2] = 0.6  # boar
        action_choice[3] = 0.7  # cow

        self.SUT.set_action_choice(action_choice)

        self._result: AnimalsToBreedActionChoice = self.SUT.process_action_choice_for_animals_to_breed(3)

    def test_then_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_hashcode_should_be_zero(self) -> None:
        self.assertEqual(self._result.hashcode, 43)

    def test_then_result_animals_to_breed_should_contain_expected_number_of_items(self) -> None:
        self.assertEqual(len(self._result.animals_to_breed), 2)

    def test_then_result_animals_to_breed_should_be_expected(self) -> None:
        self.assertListEqual(self._result.animals_to_breed, [ResourceTypeEnum.cow, ResourceTypeEnum.boar])