from typing import List, Tuple

from automated_tests.business_logic_tests.service_tests.mock_player import MockPlayer
from automated_tests.business_logic_tests.service_tests.complete_dwarf_player_choice_transfer_service_tests \
    .given_a_complete_dwarf_player_choice_transfer_service import Given_A_CompleteDwarfPlayerChoiceTransferService
from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum
from core.enums.harvest_type_enum import HarvestTypeEnum


class test_when_player_has_dwarves_of_only_one_level(Given_A_CompleteDwarfPlayerChoiceTransferService):
    def because(self) -> None:
        cards: List[BaseCard] = []

        self._dwarf_level: int = 5

        dwarves: List[Dwarf] = self.initialise_dwarves()

        self._starting_wood: int = 1

        mock_player: MockPlayer = MockPlayer(
            dwarves=dwarves,
            resources={ResourceTypeEnum.wood: self._starting_wood})
        player: Player = mock_player

        self._active_dwarves: List[Tuple[Dwarf, int]] = []

        self._result: ResultLookup[Dwarf] = self.SUT.get_dwarf(
            player,
            cards,
            2,
            3,
            HarvestTypeEnum.NoHarvest)

    def initialise_dwarves(self) -> List[Dwarf]:
        self._dwarf_1: Dwarf = self._initialise_dwarf(
            dwarf_weapon_level=self._dwarf_level,
            is_active=False)

        self._dwarf_2: Dwarf = self._initialise_dwarf(
            dwarf_weapon_level=self._dwarf_level,
            is_active=True)

        self._dwarf_3: Dwarf = self._initialise_dwarf(
            dwarf_weapon_level=self._dwarf_level,
            is_active=False)

        self._dwarves: List[Dwarf] = [self._dwarf_1, self._dwarf_2, self._dwarf_3]
        return self._dwarves

    def test_then_result_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_true(self) -> None:
        self.assertTrue(self._result.flag)

    def test_then_result_value_should_be_any_dwarf_of_lowest_level(self) -> None:
        self.assertIn(self._result.value, self._lowest_level_dwarves)

    def ignore_test_then_player_resources_should_be_unchanged(self) -> None:
        self.assertEqual(self._player.resources[ResourceTypeEnum.ruby], self._starting_rubies)

    def test_then_expected_dwarves_should_be_active(self) -> None:
        dwarf: Dwarf
        should_be_active: bool
        for (dwarf, should_be_active) in self._active_dwarves:
            with self.subTest(dwarf=dwarf):
                self.assertEqual(dwarf.is_active, should_be_active)
