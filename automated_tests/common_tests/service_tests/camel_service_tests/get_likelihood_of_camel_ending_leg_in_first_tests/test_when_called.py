import math
from functools import reduce
from typing import Dict

from automated_tests.common_tests.service_tests.camel_service_tests.given_a_camelservice import Given_A_CamelService
from common.services.camel_service import CamelColourEnum, CamelPositions, CamelStack


class Test_When_Called(Given_A_CamelService):
    def because(self) -> None:
        camel_positions: CamelPositions = CamelPositions({
            0: CamelStack([CamelColourEnum.blue, CamelColourEnum.white, CamelColourEnum.orange, CamelColourEnum.yellow]),
            12: CamelStack([CamelColourEnum.green]),
            })

        self._result: Dict[CamelColourEnum, float] = self.SUT.get_likelihood_of_camel_ending_leg_in_first(camel_positions)

        reciprocal_probability_of_blue_winning: int = math.factorial(5) * (3 ** 4)
        self._expected_probabilities: Dict[CamelColourEnum, float] = {
            CamelColourEnum.blue: 1 / reciprocal_probability_of_blue_winning,
            CamelColourEnum.white: 0,
            CamelColourEnum.orange: 0,
            CamelColourEnum.yellow: 0,
            CamelColourEnum.green: 1 - (1 / reciprocal_probability_of_blue_winning),
        }
        
    def test_then_result_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_total_probability_should_be_1(self) -> None:
        self.assertEqual(reduce(lambda x, y: x + y, self._result.values()), 1)

    def test_then_chance_of_any_camel_winning_should_be_expected(self) -> None:
        for camel, probability in self._expected_probabilities.items():
            with self.subTest(camel=camel):
                self.assertEqual(self._result[camel], probability)