from abc import ABCMeta
from typing import List
from unittest import TestCase

from automated_tests.business_logic_tests.service_tests.complete_dwarf_player_choice_transfer_service_tests.given_a_complete_dwarf_player_choice_transfer_service import \
    FakeCard
from automated_tests.mocks.mock_player import MockPlayer
from common.entities.dwarf import Dwarf
from common.services.caverna_state_service import CavernaStateService


# noinspection PyPep8Naming
from core.services.base_player_service import BasePlayerService


class Given_A_CavernaStateService(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        player_1_dwarves: List[Dwarf] = [Dwarf(), Dwarf()]
        player_2_dwarves: List[Dwarf] = [Dwarf(), Dwarf(), Dwarf(), Dwarf()]
        player_3_dwarves: List[Dwarf] = [Dwarf(), Dwarf(), Dwarf()]

        self._number_of_dwarves: int = len(player_1_dwarves) \
                                       + len(player_2_dwarves) \
                                       + len(player_3_dwarves)

        self._player1: BasePlayerService = MockPlayer(player_id=1, dwarves=player_1_dwarves)
        self._player2: BasePlayerService = MockPlayer(player_id=2, dwarves=player_2_dwarves)
        self._player3: BasePlayerService = MockPlayer(player_id=3, dwarves=player_3_dwarves)

        self.SUT: CavernaStateService = CavernaStateService(
            [self._player1, self._player2, self._player3],
            [FakeCard()])

        self.because()

    def because(self) -> None:
        pass
