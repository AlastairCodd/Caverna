from typing import List, Dict

from automated_tests.business_logic_tests.service_tests.turn_execution_service_tests.given_a_turn_execution_service import Given_A_TurnExecutionService, \
    FakeCard
from automated_tests.business_logic_tests.service_tests.turn_execution_service_tests.take_turn_tests.mock_player import MockPlayer
from buisness_logic.actions.receiveAction import ReceiveAction
from common.entities.dwarf import Dwarf
from common.entities.dwarf_card_action_combination_lookup import DwarfCardActionCombinationLookup
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum
from core.enums.harvest_type_enum import HarvestTypeEnum


class test_when_player_has_dwarves_of_only_one_level(Given_A_TurnExecutionService):
    def because(self) -> None:
        cards = self.initialise_cards()

        self._dwarf_level: int = 5

        dwarves = self.initialise_dwarves()

        self._starting_wood: int = 1

        player: Player = MockPlayer(
            dwarves=dwarves,
            resources={ResourceTypeEnum.wood: self._starting_wood}
        )

        self._number_of_active_dwarves: int = len([d for d in self._dwarves if d.is_active]) + 1

        self._actions: List[DwarfCardActionCombinationLookup] = self.initialise_actions()

        self._result: ResultLookup[Player] = self.SUT.take_turn(
            player,
            2,
            3,
            HarvestTypeEnum.NoHarvest,
            cards
        )

    def initialise_cards(self) -> List[BaseCard]:
        self._null_action_card_used_by_dwarf_2: BaseCard = FakeCard(card_id=1)

        self._received_wood: int = 2
        receive_wood_action: BaseAction = ReceiveAction({ResourceTypeEnum.wood: self._received_wood})
        self._chosen_card: BaseCard = FakeCard(card_id=2, actions=receive_wood_action)

        unused_null_action_card: BaseCard = FakeCard(card_id=3)

        cards: List[BaseCard] = [
            self._null_action_card_used_by_dwarf_2,
            self._chosen_card,
            unused_null_action_card]

        self._cards_and_active_states: Dict[BaseCard, bool] = {
            self._null_action_card_used_by_dwarf_2: True,
            self._chosen_card: True,
            unused_null_action_card: False,
        }

        return cards

    def initialise_dwarves(self) -> List[Dwarf]:
        self._dwarf_1: Dwarf = self._initialise_dwarf(
            dwarf_weapon_level=self._dwarf_level,
            is_active=False)

        self._dwarf_2: Dwarf = self._initialise_dwarf(
            dwarf_weapon_level=self._dwarf_level,
            is_active=True,
            active_card=self._null_action_card_used_by_dwarf_2)

        self._dwarf_3: Dwarf = self._initialise_dwarf(
            dwarf_weapon_level=self._dwarf_level,
            is_active=False)

        self._dwarves: List[Dwarf] = [self._dwarf_1, self._dwarf_2, self._dwarf_3]
        return self._dwarves

    def initialise_actions(self) -> List[DwarfCardActionCombinationLookup]:
        dwarf_1_action: DwarfCardActionCombinationLookup = DwarfCardActionCombinationLookup(
            self._dwarf_1,
            self._chosen_card,
            self._chosen_action
        )

        dwarf_3_action: DwarfCardActionCombinationLookup = DwarfCardActionCombinationLookup(
            self._dwarf_3,
            self._chosen_card,
            self._chosen_action
        )

        actions: List[DwarfCardActionCombinationLookup] = [
            dwarf_1_action,
            dwarf_3_action
        ]

        return actions

    def test_then_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_true(self) -> None:
        self.assertTrue(self._result.flag)

    def test_then_expected_number_of_dwarves_should_be_active(self) -> None:
        d: Dwarf
        number_of_active_dwarves = len([d for d in self._dwarves if d.is_active])
        self.assertEqual(number_of_active_dwarves, self._number_of_active_dwarves)

    def test_then_expected_cards_should_be_active(self) -> None:
        card: BaseCard
        state: bool
        for card, state in self._cards_and_active_states.items():
            with self.subTest(card=card):
                self.assertEqual(card.is_active, state)

    def test_then_activated_card_action_should_be_invoked(self) -> None:
        self.assertEqual(
            self._result.value.resources[ResourceTypeEnum.wood],
            self._starting_wood + self._received_wood)

    def test_then_result_chosen_actions_should_be_expected_length(self) -> None:
        raise NotImplementedError

    def test_then_result_chosen_actions_should_contain_expected_actions(self) -> None:
        action: DwarfCardActionCombinationLookup
        for action in self._actions:
            with self.subTest(action=action):
                self.assertIn(action, self._result.value.chosen_actions)