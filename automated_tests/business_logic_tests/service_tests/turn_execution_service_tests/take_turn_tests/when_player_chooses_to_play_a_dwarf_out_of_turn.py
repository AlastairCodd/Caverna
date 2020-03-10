from typing import List, Dict
from unittest import mock

from automated_tests.business_logic_tests.service_tests.turn_execution_service_tests.given_a_turn_execution_service import Given_A_TurnExecutionService
from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum
from core.enums.harvest_type_enum import HarvestTypeEnum


class when_player_chooses_to_play_a_dwarf_out_of_turn(Given_A_TurnExecutionService):
    def because(self) -> None:
        cards: List[BaseCard] = []

        player: Player = mock.Mock(spec=Player)

        self._dwarf_1: Dwarf = self._initialise_dwarf(dwarf_weapon_level=0)
        self._dwarf_1.is_active.return_value = False
        self._dwarf_2: Dwarf = self._initialise_dwarf(dwarf_weapon_level=2)
        self._dwarf_2.is_active.return_value = True
        self._dwarf_3: Dwarf = self._initialise_dwarf(dwarf_weapon_level=4)
        self._dwarf_3.is_active.return_value = False

        self._player_dwarves: List[Dwarf] = [self._dwarf_1, self._dwarf_2, self._dwarf_3]
        player.dwarves.return_value = self._player_dwarves

        self._starting_rubies: int = 4
        player_resources: Dict[ResourceTypeEnum, int] = {ResourceTypeEnum.ruby: self._starting_rubies, ResourceTypeEnum.wood: 3}
        player.resources.return_value = player_resources

        player.get_player_choice_use_dwarf_out_of_order.return_value = ResultLookup(True, self._dwarf_3)

        self._result: ResultLookup[Player] = ResultLookup(errors="false")
            # self.SUT.take_turn(player, 4, 2, HarvestTypeEnum.Harvest, cards)

    def test_then_result_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_true(self) -> None:
        self.assertTrue(self._result.flag)

    def test_then_player_resources_should_contain_one_fewer_ruby(self) -> None:
        self.assertEqual(self._result.value.resources[ResourceTypeEnum.ruby], self._starting_rubies - 1)

    def test_then_player_chosen_dwarf_should_be_active(self) -> None:
        self.assertTrue(self._dwarf_3.is_active)

    def test_then_errors_should_contain_expected_errors(self) -> None:
        dwarf: Dwarf
        state: bool
        dwarves_and_active_states: Dict[Dwarf, bool] = {
            self._dwarf_1: False,
            self._dwarf_2: True,
            self._dwarf_3: True,
        }
        for dwarf, state in dwarves_and_active_states.items():
            with self.subTest(dwarf=dwarf):
                self.assertEqual(dwarf.is_active(), state)
