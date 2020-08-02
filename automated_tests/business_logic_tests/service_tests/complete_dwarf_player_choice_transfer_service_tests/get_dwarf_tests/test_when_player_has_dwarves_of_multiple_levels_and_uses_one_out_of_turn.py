from typing import List, Dict

from automated_tests.business_logic_tests.service_tests.complete_dwarf_player_choice_transfer_service_tests \
    .given_a_complete_dwarf_player_choice_transfer_service import Given_A_CompleteDwarfPlayerChoiceTransferService
from automated_tests.business_logic_tests.service_tests.mock_player import MockPlayer
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from core.enums.caverna_enums import ResourceTypeEnum
from core.services.base_player_service import BasePlayerService


class test_when_player_has_dwarves_of_multiple_levels_and_uses_one_out_of_turn(Given_A_CompleteDwarfPlayerChoiceTransferService):
    def because(self) -> None:
        dwarves: List[Dwarf] = self.initialise_dwarves()
        self._chosen_dwarf: Dwarf = self._dwarf_2

        self._starting_rubies: int = 4
        resources: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.ruby: self._starting_rubies,
            ResourceTypeEnum.wood: 3
        }

        mock_player = MockPlayer(
            dwarves=dwarves,
            resources=resources
        )
        self._player: BasePlayerService = mock_player

        mock_player.get_player_choice_use_dwarf_out_of_order_returns(
            lambda info_dwarves, info_cards, info_turn_index, info_round_index, info_harvest_type: ResultLookup(True, True)
        )

        mock_player.get_player_choice_dwarf_to_use_out_of_order_returns(
            lambda info_dwarves, info_cards, info_turn_index, info_round_index, info_harvest_type: ResultLookup(True, self._chosen_dwarf)
        )

        self._result: ResultLookup[Dwarf] = self.SUT.get_dwarf(self._player, self._turn_descriptor)

    def initialise_dwarves(self):
        self._dwarf_1: Dwarf = self._initialise_dwarf(
            dwarf_weapon_level=0,
            is_active=False)

        self._dwarf_2: Dwarf = self._initialise_dwarf(
            dwarf_weapon_level=2,
            is_active=False)

        self._dwarf_3: Dwarf = self._initialise_dwarf(
            dwarf_weapon_level=4,
            is_active=False)

        dwarves: List[Dwarf] = [self._dwarf_1, self._dwarf_2, self._dwarf_3]
        return dwarves

    def test_then_result_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_false(self) -> None:
        self.assertFalse(self._result.flag)

    def test_then_result_value_should_be_chosen_dwarf(self) -> None:
        self.assertIs(self._result.value, self._chosen_dwarf)

    def test_then_result_errors_should_contain_expected_errors(self) -> None:
        self.assertIn("player chose a dwarf that is already active", self._result.errors)

    def ignore_test_then_player_resources_should_be_reduced(self) -> None:
        self.assertEqual(self._player.resources[ResourceTypeEnum.ruby], self._starting_rubies - 1)