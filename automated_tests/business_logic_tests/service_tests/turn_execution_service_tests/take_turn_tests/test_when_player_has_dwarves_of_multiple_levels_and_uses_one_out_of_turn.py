from typing import List, Dict

from automated_tests.business_logic_tests.service_tests.turn_execution_service_tests.given_a_turn_execution_service import Given_A_TurnExecutionService, \
    FakeCard
from automated_tests.business_logic_tests.service_tests.turn_execution_service_tests.take_turn_tests.mock_player import MockPlayer
from buisness_logic.actions.receiveAction import ReceiveAction
from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum
from core.enums.harvest_type_enum import HarvestTypeEnum


class test_when_player_has_dwarves_of_multiple_levels_and_uses_one_out_of_turn(Given_A_TurnExecutionService):
    def because(self) -> None:
        cards = self.initialise_cards()

        dwarves = self.initialise_dwarves()

        self._dwarves_and_active_states: Dict[Dwarf, bool] = {
            self._dwarf_1: False,
            self._dwarf_2: True,
            self._dwarf_3: True,
        }

        self._starting_rubies: int = 4
        resources: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.ruby: self._starting_rubies,
            ResourceTypeEnum.wood: 3
        }

        player: Player = MockPlayer(
            dwarves=dwarves,
            resources=resources
        )

        self._result: ResultLookup[Player] = self.SUT.take_turn(
            player,
            1,
            2,
            HarvestTypeEnum.Harvest,
            cards
        )

    def initialise_dwarves(self):
        self._dwarf_1: Dwarf = self._initialise_dwarf(
            dwarf_weapon_level=0,
            is_active=False)

        self._dwarf_2: Dwarf = self._initialise_dwarf(
            dwarf_weapon_level=2,
            is_active=True,
            active_card=self._null_action_card_used_by_dwarf_2)

        self._dwarf_3: Dwarf = self._initialise_dwarf(
            dwarf_weapon_level=4,
            is_active=False)

        dwarves: List[Dwarf] = [self._dwarf_1, self._dwarf_2, self._dwarf_3]
        return dwarves

    def initialise_cards(self) -> List[BaseCard]:
        self._null_action_card_used_by_dwarf_2: BaseCard = FakeCard(card_id=1)

        receive_wood_action: BaseAction = ReceiveAction({ResourceTypeEnum.wood: 1})
        self._chosen_card: BaseCard = FakeCard(card_id=2, actions=receive_wood_action)

        unused_null_action_card: BaseCard = FakeCard(card_id=3)

        cards: List[BaseCard] = [
            self._null_action_card_used_by_dwarf_2,
            self._chosen_card,
            unused_null_action_card]

        return cards

    def test_then_result_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_true(self) -> None:
        self.assertTrue(self._result.flag)

    def test_then_player_resources_should_contain_one_fewer_ruby(self) -> None:
        self.assertEqual(self._result.value.resources[ResourceTypeEnum.ruby], self._starting_rubies - 1)

    def test_then_player_chosen_dwarf_should_be_active(self) -> None:
        self.assertTrue(self._dwarf_3.is_active)

    def test_then_expected_dwarves_should_be_active(self) -> None:
        dwarf: Dwarf
        state: bool
        for dwarf, state in self._dwarves_and_active_states.items():
            with self.subTest(dwarf=dwarf):
                self.assertEqual(dwarf.is_adult, state)
