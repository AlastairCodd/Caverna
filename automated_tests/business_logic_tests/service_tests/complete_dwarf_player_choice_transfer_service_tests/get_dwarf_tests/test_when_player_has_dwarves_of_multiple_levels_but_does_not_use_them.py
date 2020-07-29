from typing import Dict, List

from automated_tests.business_logic_tests.service_tests.mock_player import MockPlayer
from automated_tests.business_logic_tests.service_tests.complete_dwarf_player_choice_transfer_service_tests\
    .given_a_complete_dwarf_player_choice_transfer_service import Given_A_CompleteDwarfPlayerChoiceTransferService
from common.entities.dwarf import Dwarf
from core.services.base_player_service import BasePlayerService
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum
from core.enums.harvest_type_enum import HarvestTypeEnum


class test_when_player_has_dwarves_of_multiple_levels_but_does_not_use_them(Given_A_CompleteDwarfPlayerChoiceTransferService):
    def because(self) -> None:
        cards: List[BaseCard] = []

        dwarves: List[Dwarf] = self.initialise_dwarves()
        self._lowest_level_dwarves: List[Dwarf] = [self._dwarf_1, self._dwarf_2]

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
            lambda info_dwarves, info_cards, info_turn_index, info_round_index, info_harvest_type: ResultLookup(True, False)
        )

        self._result: ResultLookup[Dwarf] = self.SUT.get_dwarf(
            self._player,
            cards,
            1,
            2,
            HarvestTypeEnum.Harvest,
        )

    def initialise_dwarves(self):
        self._dwarf_1: Dwarf = self._initialise_dwarf(
            dwarf_weapon_level=1,
            is_active=False)

        self._dwarf_2: Dwarf = self._initialise_dwarf(
            dwarf_weapon_level=1,
            is_active=False)

        self._dwarf_3: Dwarf = self._initialise_dwarf(
            dwarf_weapon_level=4,
            is_active=False)

        self._dwarf_4: Dwarf = self._initialise_dwarf(
            dwarf_weapon_level=1,
            is_active=True)

        dwarves: List[Dwarf] = [self._dwarf_1, self._dwarf_2, self._dwarf_3]
        return dwarves

    def test_then_result_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_true(self) -> None:
        self.assertTrue(self._result.flag)

    def test_then_result_value_should_be_any_dwarf_of_lowest_level(self) -> None:
        self.assertIn(self._result.value, self._lowest_level_dwarves)

    def ignore_test_then_player_resources_should_be_unchanged(self) -> None:
        self.assertEqual(self._player.resources[ResourceTypeEnum.ruby], self._starting_rubies)
