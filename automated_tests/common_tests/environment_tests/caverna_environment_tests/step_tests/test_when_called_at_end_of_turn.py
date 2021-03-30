from automated_tests.common_tests.environment_tests.caverna_environment_tests.given_a_caverna_environment import Given_A_CavernaEnv


class test_when_called_at_end_of_turn(Given_A_CavernaEnv):
    def because(self) -> None:
        self.SUT.reset()

        # player 1 turn 1
        self.SUT.step()
        # player 2 turn 1
        self.SUT.step()
        # player 1 turn 2
        self.SUT.step()
        # player 2 turn 2
        self.SUT.step()

    def test_then_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self.SUT)
