from automated_tests.common_tests.entity_tests.multi_variable_polynomial_tests.given_a_polynomial import Given_A_MultiVariablePolynomial
from common.entities.multi_variable_polynomial import MultiVariablePolynomial, Monomial


class test_when_all_parameters_are_valid(Given_A_MultiVariablePolynomial):
    def because(self) -> None:
        self._result: MultiVariablePolynomial = MultiVariablePolynomial(
            {
                Monomial(
                    {
                        "x": 2,
                    }
                ): 1,
                Monomial(
                    {
                        "y": 2,
                    }
                ): 2,
                Monomial(
                    {
                        "x": 1,
                        "y": 1,
                    }
                ): 2,
            }
        )

    def test_then_result_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._result)
