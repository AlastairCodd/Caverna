from typing import cast, Dict, List

from automated_tests.business_logic_tests.action_tests.convert_single_action_tests.given_a_convert_single_action import Given_A_ConvertSingleAction
from automated_tests.mocks.mock_player import MockPlayer
from automated_tests.mocks.mock_tile import MockTile
from buisness_logic.actions.convert_single_action import ConvertSingleAction
from buisness_logic.effects.conversion_effects import ConvertEffect
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository


class test_when_only_one_conversion_effect_applies_and_is_used_multiple_times(Given_A_ConvertSingleAction):
    def because(self) -> None:
        self.SUT = ConvertSingleAction(
            [ResourceTypeEnum.donkey],
            [ResourceTypeEnum.food],
            5)

        self._player: BasePlayerRepository = self.initialise_player()

        self._result: ResultLookup[int] = self.SUT.invoke(
            self._player,
            None,
            None)

    def initialise_player(self) -> BasePlayerRepository:
        starting_resources: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.donkey: 7
        }

        player: MockPlayer = MockPlayer(resources=starting_resources)

        conversion_single_effect: ConvertEffect = ConvertEffect(
            {ResourceTypeEnum.donkey: 1},
            {ResourceTypeEnum.food: 1}
        )
        conversion_double_effect: ConvertEffect = ConvertEffect(
            {ResourceTypeEnum.donkey: 2},
            {ResourceTypeEnum.food: 3}
        )

        conversion_tile: BaseTile = MockTile(effects=[conversion_single_effect, conversion_double_effect])
        player.tiles[28].set_tile(conversion_tile)

        self._expected_resources: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.donkey: 2,
            ResourceTypeEnum.food: 7
        }

        return player

    def test_then_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_true(self) -> None:
        self.assertTrue(self._result.flag)

    def test_then_result_value_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result.value)

    def test_then_result_value_should_be_expected(self) -> None:
        self.assertEqual(self._result.value, 7)

    def test_then_result_errors_should_be_empty(self) -> None:
        self.assertListEqual(cast(list, self._result.errors), [])

    def test_then_player_resources_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._player.resources)

    def test_then_player_resources_should_not_be_empty(self) -> None:
        self.assertGreater(len(cast(List, self._player.resources)), 0)

    def test_then_player_resources_should_contain_expected_resources(self) -> None:
        for resource in self._expected_resources:
            with self.subTest(resources=resource):
                self.assertEqual(self._player.resources[resource], self._expected_resources[resource])
