from typing import Dict, List, cast

from automated_tests.business_logic_tests.effects_tests.purchase_effects_tests.allow_substitution_for_purchase_tests\
    .given_a_allowsubstitutionforpurchase import Given_An_AllowSubstitutionForPurchase
from core.enums.caverna_enums import ResourceTypeEnum


class Test_When_Substitute_For_Not_Contained(Given_An_AllowSubstitutionForPurchase):
    def because(self) -> None:
        self._given_current_price: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.cow: 3,
            ResourceTypeEnum.wood: 2,
            ResourceTypeEnum.coin: 12
        }

        self._substitute_for: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.stone: 2,
            ResourceTypeEnum.wood: 1,
        }
        self._substitute_with: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.grain: 1,
            ResourceTypeEnum.coin: 4,
        }

        self._result = self.SUT.invoke(
            self._given_current_price)

    def test_then_result_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_should_not_be_empty(self) -> None:
        self.assertGreater(len(cast(List, self._result)), 0)

    def test_then_result_should_contain_expected_resources(self) -> None:
        for resource in self._given_current_price:
            with self.subTest(resources=resource):
                self.assertEqual(self._result[resource], self._given_current_price[resource])
