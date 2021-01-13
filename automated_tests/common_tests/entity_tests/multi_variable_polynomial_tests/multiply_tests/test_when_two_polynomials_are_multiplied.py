from unittest import TestCase

from automated_tests.common_tests.entity_tests.multi_variable_polynomial_tests.given_a_polynomial import Given_A_MultiVariablePolynomial
from common.entities.multi_variable_polynomial import MultiVariablePolynomial, Monomial


class test_when_two_are_added(Given_A_MultiVariablePolynomial):
    def because(self) -> None:
        a: MultiVariablePolynomial = MultiVariablePolynomial(
            {
                Monomial(
                    {
                        "s": 2,
                    }
                ): 1,
                Monomial(
                    {
                        "d": 2
                    }
                ): 1,
                Monomial(
                    {
                        "c": 2
                    }
                ): 1,
            }
        )
        b: MultiVariablePolynomial = MultiVariablePolynomial(
            {
                Monomial(
                    {
                        "s": 3,
                    }
                ): 1,
                Monomial(
                    {
                        "d": 2
                    }
                ): 1,
                Monomial(
                    {
                        "c": 2
                    }
                ): 1,
            }
        )
        self._result: MultiVariablePolynomial = a * b
        self._reversed_result: MultiVariablePolynomial = b * a
        self._expected: MultiVariablePolynomial = MultiVariablePolynomial(
            {
                Monomial("sssss"): 1,
                Monomial("sscc"): 1,
                Monomial("ssdd"): 1,
                Monomial("ssscc"): 1,
                Monomial("cccc"): 1,
                Monomial("ccdd"): 2,
                Monomial("sssdd"): 1,
                Monomial("dddd"): 1,
            }
        )

    def test_then_result_should_have_expected_terms(self) -> None:
        for variable, coefficient in self._expected.terms.items():
            with self.subTest(variable=str(variable)):
                self.assertEqual(self._result.get_coefficient_for_variable(variable), coefficient)
