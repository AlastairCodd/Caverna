from typing import List, Dict

from automated_tests.business_logic_tests.service_tests.complete_dwarf_player_choice_transfer_service_tests.get_dwarf_tests.mock_player import MockPlayer
from automated_tests.business_logic_tests.service_tests.complete_dwarf_player_choice_transfer_service_tests\
    .given_a_complete_dwarf_player_choice_transfer_service import Given_A_CompleteDwarfPlayerChoiceTransferService
from common.entities.dwarf import Dwarf
from common.entities.player import Player
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum
from core.enums.harvest_type_enum import HarvestTypeEnum


class test_when_player_does_not_have_any_dwarves_remaining(Given_A_CompleteDwarfPlayerChoiceTransferService):
    def because(self) -> None:
        self._expected_errors: List[str] = ["Player has used all dwarves"]

        self._cards: List[BaseCard] = []

        dwarves: List[Dwarf] = []
        resources: Dict[ResourceTypeEnum, int] = {ResourceTypeEnum.ruby: 2}
        self._player: Player = MockPlayer(dwarves, resources)

    def test_then_an_out_of_range_error_should_be_raised(self):
        self.assertRaises(IndexError, lambda: self.SUT.get_dwarf(self._player, self._cards, 4, 2, HarvestTypeEnum.Harvest))