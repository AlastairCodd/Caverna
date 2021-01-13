from automated_tests.common_tests.entity_tests.multi_variable_polynomial_tests.given_a_polynomial import Given_A_MultiVariablePolynomial
from common.entities.multi_variable_polynomial import MultiVariablePolynomial, Monomial


class test_when_constructed_from_strings(Given_A_MultiVariablePolynomial):
    def because(self) -> None:
        self._result: MultiVariablePolynomial = MultiVariablePolynomial(
            {
                Monomial("xx"): 1,
                Monomial("yy"): 2,
                Monomial("xy"): 2,
            }
        )

    def test_then_result_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._result)
