from typing import Dict, List, Union

from automated_tests.business_logic_tests.effects_tests.purchase_effects_tests.allow_substitution_for_purchase_tests\
    .given_a_allowsubstitutionforpurchase import Given_An_AllowSubstitutionForPurchase
from automated_tests.mocks.mock_player import MockPlayer
from automated_tests.mocks.mock_tile import MockTile
from common.entities.player import Player
from common.entities.weapon import Weapon
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum


class MockDiscountPlayer(MockPlayer):
    def get_player_choice_discount(
            self,
            possible_prices: List[Dict[ResourceTypeEnum, int]],
            target: Union[BaseTile, Weapon]) \
            -> Dict[ResourceTypeEnum, int]:
        return possible_prices[2]


class Test_When_Substitute_For_Contained_Multiple_Times(Given_An_AllowSubstitutionForPurchase):
    def because(self) -> None:
        self._player: Player = MockDiscountPlayer(3)
        self._tile: BaseTile = MockTile()
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

        self._result: Dict[ResourceTypeEnum, int] = self.SUT.invoke(
            self._player,
            self._tile,
            self._given_current_price)

    def test_then_result_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_should_not_be_empty(self) -> None:
        self.assertGreater(len(self._result), 0)

    def test_then_result_should_be_the_correct_length(self) -> None:
        self.assertCountEqual(self._result, self._expected)

    def test_then_result_should_be_expected(self) -> None:
        self.assertDictEqual(self._result, self._expected)
