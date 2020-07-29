from typing import Dict

from automated_tests.business_logic_tests.effects_tests.purchase_effects_tests.allow_substitution_for_purchase_tests\
    .given_a_allowsubstitutionforpurchase import Given_An_AllowSubstitutionForPurchase
from automated_tests.mocks.mock_player import MockPlayer
from automated_tests.mocks.mock_tile import MockTile
from core.services.base_player_service import BasePlayerService
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum


class Test_When_Substitute_For_Not_Contained(Given_An_AllowSubstitutionForPurchase):
    def because(self) -> None:
        self._player: BasePlayerService = MockPlayer(4)
        self._tile: BaseTile = MockTile()
        self._given_current_price: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.cow: 3,
            ResourceTypeEnum.wood: 2,
            ResourceTypeEnum.coin: 12
        }

        self._result = self.SUT.invoke(
            self._player,
            self._tile,
            self._given_current_price)

        self._result = self.SUT.invoke(
            self._player,
            self._tile,
            self._given_current_price
        )

    def test_then_result_should_not_be_none(self):
        self.assertIsNotNone(self._result)

    def test_then_result_should_not_be_empty(self) -> None:
        self.assertGreater(len(self._result), 0)

    def test_then_result_should_be_the_correct_length(self) -> None:
        self.assertCountEqual(self._result, self._given_current_price)

    def test_then_result_should_be_given_current_price(self):
        self.assertEqual(self._result, self._given_current_price)
