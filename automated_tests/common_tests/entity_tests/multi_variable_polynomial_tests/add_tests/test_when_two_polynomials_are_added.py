from unittest import TestCase

from automated_tests.common_tests.entity_tests.multi_variable_polynomial_tests.given_a_polynomial import Given_A_MultiVariablePolynomial
from common.entities.multi_variable_polynomial import MultiVariablePolynomial, Monomial


class test_when_two_are_added(Given_A_MultiVariablePolynomial):
    def because(self) -> None:
        a: MultiVariablePolynomial = MultiVariablePolynomial(
            {
                Monomial(
                    {
                        "x": 2,
                    }
                ): 1,
                Monomial(
                    {
                        "x": 1,
                        "y": 1,
                    }
                ): 1,
            }
        )
        b: MultiVariablePolynomial = MultiVariablePolynomial(
            {
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
                ): 1,
            }
        )
        self._result: MultiVariablePolynomial = a + b
        self._expected: MultiVariablePolynomial = MultiVariablePolynomial(
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

    def test_then_result_should_have_expected_terms(self) -> None:
        for variable, coefficient in self._expected.terms.items():
            with self.subTest(variable=variable):
                self.assertEqual(self._result.get_coefficient_for_variable(variable), coefficient)
