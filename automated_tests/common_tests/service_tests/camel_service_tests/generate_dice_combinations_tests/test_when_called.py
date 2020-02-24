from typing import Dict, List

from automated_tests.common_tests.service_tests.camel_service_tests.given_a_camelservice import Given_A_CamelService
from common.services.camel_service import CamelService, CamelColourEnum


class Test_When_called(Given_A_CamelService):
    def because(self) -> None:
        camel_dice: Dict[CamelColourEnum, Dict[int, int]] = {
            CamelColourEnum.blue: {5: 1, 6: 1, 7: 1},
            CamelColourEnum.orange: {8: 1, 9: 1},
            CamelColourEnum.white: {10: 1, 11: 1},
        }
        self.SUT = CamelService(camel_dice=camel_dice)
        self._result: List[Dict[CamelColourEnum, int]] = list(self.SUT._generate_dice_combinations())

        self._expected_dice_combinations: List[Dict[CamelColourEnum, int]] = [
            {CamelColourEnum.blue: 5, CamelColourEnum.orange: 8, CamelColourEnum.white: 10},
            {CamelColourEnum.blue: 5, CamelColourEnum.orange: 8, CamelColourEnum.white: 11},
            {CamelColourEnum.blue: 5, CamelColourEnum.orange: 9, CamelColourEnum.white: 10},
            {CamelColourEnum.blue: 5, CamelColourEnum.orange: 9, CamelColourEnum.white: 11},
            {CamelColourEnum.blue: 6, CamelColourEnum.orange: 8, CamelColourEnum.white: 10},
            {CamelColourEnum.blue: 6, CamelColourEnum.orange: 8, CamelColourEnum.white: 11},
            {CamelColourEnum.blue: 6, CamelColourEnum.orange: 9, CamelColourEnum.white: 10},
            {CamelColourEnum.blue: 6, CamelColourEnum.orange: 9, CamelColourEnum.white: 11},
            {CamelColourEnum.blue: 7, CamelColourEnum.orange: 8, CamelColourEnum.white: 10},
            {CamelColourEnum.blue: 7, CamelColourEnum.orange: 8, CamelColourEnum.white: 11},
            {CamelColourEnum.blue: 7, CamelColourEnum.orange: 9, CamelColourEnum.white: 10},
            {CamelColourEnum.blue: 7, CamelColourEnum.orange: 9, CamelColourEnum.white: 11},
        ]

    def test_then_result_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_should_be_correct_length(self) -> None:
        self.assertCountEqual(self._result, self._expected_dice_combinations)

    def test_then_result_should_contain_expected_values(self) -> None:
        for dice_combination in self._expected_dice_combinations:
            with self.subTest(dice_combination=dice_combination):
                self.assertIn(dice_combination, self._result)
