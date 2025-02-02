from typing import List, cast

from automated_tests.business_logic_tests.service_tests.turn_execution_service_tests.given_a_turn_execution_service import FakeCard
from automated_tests.common_tests.service_tests.caverna_state_service_tests.given_a_caverna_state_service import Given_A_CavernaStateService
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.enums.harvest_type_enum import HarvestTypeEnum
from core.services.base_player_service import BasePlayerService


class test_when_all_players_have_been_for_turn(Given_A_CavernaStateService):
    def because(self) -> None:
        fake_card: BaseCard = FakeCard()
        self.SUT.increment_round_index(fake_card, HarvestTypeEnum.Harvest, logging=False)

        self._expected_player_order: List[BasePlayerService] = [
            self._player1,
            self._player2,
            self._player3,
            self._player1,
            self._player2,
            self._player3]

        self._players_in_order: List[BasePlayerService] = []

        for _ in range(len(self._expected_player_order)):
            next_player_result: ResultLookup[BasePlayerService] = self.SUT.get_next_player()
            if next_player_result.flag:
                next_player: BasePlayerService = next_player_result.value
                self._players_in_order.append(next_player)

                remaining_dwarves_for_player: List[Dwarf] = [dwarf for dwarf in next_player.dwarves if dwarf.is_adult and not dwarf.is_active]
                next_dwarf: Dwarf = remaining_dwarves_for_player[0]
                next_dwarf.set_active(fake_card)
            else:
                raise EOFError()

    def test_then_expected_number_of_players_should_have_turns(self) -> None:
        self.assertEqual(len(self._players_in_order), len(self._expected_player_order))

    def test_then_players_in_order_should_match_expected_order(self) -> None:
        self.assertListEqual(self._players_in_order, self._expected_player_order)

    def test_then_turn_index_should_be_expected(self) -> None:
        self.assertEqual(self.SUT.turn_index, 1)
