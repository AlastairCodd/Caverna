import math
from typing import Dict, List

from automated_tests.common_tests.service_tests.camel_service_tests.given_a_camelservice import Given_A_CamelService
from common.services.camel_service import CamelColourEnum, OrderedDice, CamelPositions, CamelStack


class Test_When_called(Given_A_CamelService):
    def because(self) -> None:
        camel_positions: CamelPositions = CamelPositions({
            0: CamelStack([CamelColourEnum.blue, CamelColourEnum.green]),
            1: CamelStack([CamelColourEnum.yellow, CamelColourEnum.orange]),
            2: CamelStack([CamelColourEnum.white]),
        })
        self._result: Dict[CamelPositions, List[OrderedDice]] = self.SUT.get_possible_positions_for_camels(camel_positions)
        self._expected_number_of_results: int = math.factorial(5) * 3 ** 5
        
    def test_then_result_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._result)
        
    def test_then_result_should_contain_expected_number_of_entries(self) -> None:
        self.assertEqual(self._result, self._expected_number_of_results)