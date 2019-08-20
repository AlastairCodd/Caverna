from automated_tests.common_tests.service_tests.conditional_service_tests.mockBaseAction import MockBaseAction
from automated_tests.common_tests.service_tests.conditional_service_tests.test_conditionalService import \
    Given_A_Conditional_Service
from core.baseClasses.base_action import BaseAction


# noinspection PyPep8Naming
class Test_When_Parameter_Is_BaseAction(Given_A_Conditional_Service):
    def because(self):
        self.base_action: BaseAction = MockBaseAction()
        self.result = self.SUT.get_possible_choices(self.base_action)

    def test_then_the_result_should_not_be_null(self):
        self.assertIsNotNone(self.result)

    def test_then_the_result_should_not_be_empty(self):
        self.assertGreater(len(self.result), 0)

    def test_then_the_result_should_contain_one_item(self):
        self.assertEqual(len(self.result), 1)

    def test_then_the_result_should_contain_the_expected_result(self):
        self.assertIn([self.base_action], self.result)
