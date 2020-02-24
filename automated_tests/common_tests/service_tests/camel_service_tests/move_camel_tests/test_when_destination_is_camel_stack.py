from typing import Dict, List

from automated_tests.common_tests.service_tests.camel_service_tests.given_a_camelservice import Given_A_CamelService
from common.entities.result_lookup import ResultLookup
from common.services.camel_service import CamelColourEnum, OasisTypeEnum


class test_when_destination_is_camel_stack(Given_A_CamelService):
    def because(self) -> None:
        camel_positions: Dict[int, List[CamelColourEnum]] = {
            3: [CamelColourEnum.yellow, CamelColourEnum.blue, CamelColourEnum.green],
            4: [CamelColourEnum.white],
            5: [CamelColourEnum.orange],
        }

        self._expected_positions: Dict[int, List[CamelColourEnum]] = {
            3: [CamelColourEnum.green],
            4: [CamelColourEnum.white],
            5: [CamelColourEnum.yellow, CamelColourEnum.blue, CamelColourEnum.orange],
        }

        self._result: ResultLookup[Dict[int, List[CamelColourEnum]]] = self.SUT._move_camel(
            CamelColourEnum.blue,
            2,
            camel_positions
        )

    def test_then_result_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_true(self) -> None:
        self.assertTrue(self._result.flag)

    def test_then_result_value_should_be_expected(self) -> None:
        for position, stack in self._expected_positions.items():
            with self.subTest(position=position):
                self.assertListEqual(self._result.value[position], stack)