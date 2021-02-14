from typing import Dict, List, cast

from automated_tests.business_logic_tests.effects_tests.purchase_effects_tests.allow_substitution_for_purchase_tests\
    .given_a_allowsubstitutionforpurchase import Given_An_AllowSubstitutionForPurchase
from core.enums.caverna_enums import ResourceTypeEnum


class Test_When_Substitute_For_Contained_Multiple_Times(Given_An_AllowSubstitutionForPurchase):
    def because(self) -> None:
        self._given_current_price: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.stone: 5,
            ResourceTypeEnum.wood: 2
        }

        self._expected: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.stone: 1,
            ResourceTypeEnum.wood: 0,
            ResourceTypeEnum.grain: 2,
            ResourceTypeEnum.coin: 8,
        }

        self._substitute_for: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.stone: 2,
            ResourceTypeEnum.wood: 1,
        }
        self._substitute_with: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.grain: 1,
            ResourceTypeEnum.coin: 4,
        }

        intermediate_result: Dict[ResourceTypeEnum, int] = self.SUT.invoke(self._given_current_price)

        self._result: Dict[ResourceTypeEnum, int] = self.SUT.invoke(intermediate_result)

    def test_then_result_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_should_not_be_empty(self) -> None:
        self.assertGreater(len(cast(List, self._result)), 0)

    def test_then_result_should_contain_expected_resources(self) -> None:
        for resource in self._expected:
            with self.subTest(resources=resource):
                self.assertEqual(self._result[resource], self._expected[resource])
