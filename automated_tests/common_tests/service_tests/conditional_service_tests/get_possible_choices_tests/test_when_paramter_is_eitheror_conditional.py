from typing import Iterable, List
from automated_tests.common_tests.service_tests.conditional_service_tests.mockBaseAction import MockBaseAction
from automated_tests.common_tests.service_tests.conditional_service_tests.test_conditionalService import \
    Given_A_Conditional_Service
from common.entities.multiconditional import Conditional
from core.baseClasses.base_action import BaseAction
from core.enums.caverna_enums import ActionCombinationEnum


# noinspection PyPep8Naming
class Test_When_Parameter_Is_EitherOr_Conditional(Given_A_Conditional_Service):
    def because(self):
        self.action1: BaseAction = MockBaseAction()
        self.action2: BaseAction = MockBaseAction()

        self.conditional: Conditional = Conditional(
            ActionCombinationEnum.EitherOr,
            self.action1,
            self.action2)

        self.combinations: Iterable[List[BaseAction]] = [
            [self.action1],
            [self.action2]
        ]

        self.result = self.SUT.get_possible_choices(self.conditional)

    def test_then_the_result_should_not_be_null(self):
        self.assertIsNotNone(self.result)

    def test_then_the_result_should_not_be_empty(self):
        self.assertGreater(len(self.result), 0)

    def test_then_the_result_should_contain_one_item(self):
        self.assertEqual(self.result, self.combinations)

    def test_then_the_result_should_contain_the_expected_combinations(self):
        for combination in self.combinations:
            with self.subTest():
                self.assertIn(combination, self.result)
