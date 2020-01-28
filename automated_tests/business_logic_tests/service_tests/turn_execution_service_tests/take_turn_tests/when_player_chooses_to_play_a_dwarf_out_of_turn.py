from typing import List
from unittest import mock

from automated_tests.business_logic_tests.service_tests.turn_execution_service_tests.given_a_turn_execution_service import Given_A_TurnExecutionService
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.enums.harvest_type_enum import HarvestTypeEnum


class when_player_chooses_to_play_a_dwarf_out_of_turn(Given_A_TurnExecutionService):
    def because(self) -> None:
        self._expected_errors: List[str] = ["Invalid dwarf id "]

        cards: List[BaseCard] = []

        player: Player = mock.Mock(spec=Player)
        self._result: ResultLookup[Player] = self.SUT.take_turn(player, 4, 2, HarvestTypeEnum.Harvest, cards)

    def test_then_result_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_false(self) -> None:
        self.assertFalse(self._result.flag)

    def test_then_errors_should_contain_expected_errors(self) -> None:
        error: str
        for error in self._expected_errors:
            with self.subTest(error=error):
                self.assertIn(error, self._result.errors)
