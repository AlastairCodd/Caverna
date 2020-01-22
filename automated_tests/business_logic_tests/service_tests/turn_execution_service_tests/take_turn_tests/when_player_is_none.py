from automated_tests.business_logic_tests.service_tests.turn_execution_service_tests.given_a_turn_execution_service import Given_A_TurnExecutionService


class Test_When_player_Is_Null(Given_A_TurnExecutionService):
    def test_Then_A_ValueError_Should_Be_Thrown(self):
        self.assertRaises(ValueError, self.SUT.take_turn, None)
