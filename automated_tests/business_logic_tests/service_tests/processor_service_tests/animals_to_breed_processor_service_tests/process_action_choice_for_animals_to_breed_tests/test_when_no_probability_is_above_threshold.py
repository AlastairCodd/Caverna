from automated_tests.business_logic_tests.service_tests.processor_service_tests.animals_to_breed_processor_service_tests.given_an_animals_to_breed_action_choice_processor_service import \
    Given_A_AnimalsToBreedActionChoiceProcessorService
from buisness_logic.services.processor_services.animals_to_breed_action_choice_processor_service import AnimalsToBreedActionChoice


class test_when_no_probability_is_above_threshold(Given_A_AnimalsToBreedActionChoiceProcessorService):
    def because(self) -> None:
        self.SUT.offset = 0
        self.SUT.set_action_choice([0.1 for _ in range(self.SUT.length)])

        self._result: AnimalsToBreedActionChoice = self.SUT.process_action_choice_for_animals_to_breed(3)

    def test_then_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_hashcode_should_be_zero(self) -> None:
        self.assertEqual(self._result.hashcode, 0)

    def test_then_result_animals_to_breed_should_be_empty(self) -> None:
        self.assertEqual(len(self._result.animals_to_breed), 0)

