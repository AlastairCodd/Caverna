from automated_tests.common_tests.environment_tests.caverna_environment_tests.given_a_caverna_environment import Given_A_CavernaEnv


class test_when_reset(Given_A_CavernaEnv):
    def because(self) -> None:
        self.SUT.reset()

    def test_then_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self.SUT)