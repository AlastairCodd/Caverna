from typing import List, cast

from automated_tests.business_logic_tests.action_tests.go_on_an_expedition_action.given_a_go_on_expedition_action import \
    Given_A_GoOnAnExpeditionAction
from automated_tests.business_logic_tests.service_tests.complete_dwarf_player_choice_transfer_service_tests \
    .given_a_complete_dwarf_player_choice_transfer_service import FakeCard
from automated_tests.mocks.mock_player import MockPlayer
from buisness_logic.actions.pay_action import PayAction
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.enums.caverna_enums import ResourceTypeEnum
from core.enums.harvest_type_enum import HarvestTypeEnum
from core.services.base_player_service import BasePlayerService


class test_when_chosen_actions_are_not_possible(Given_A_GoOnAnExpeditionAction):
    def because(self) -> None:
        player: BasePlayerService = self.initialise_player()

        dwarf: Dwarf = Dwarf(True)

        turn_descriptor: TurnDescriptorLookup = TurnDescriptorLookup(
            [FakeCard()],
            [],
            1,
            2,
            HarvestTypeEnum.Harvest)

        self._result: ResultLookup[ActionChoiceLookup] = self.SUT.set_player_choice(
            player,
            dwarf,
            turn_descriptor
        )

    def initialise_player(self) -> BasePlayerService:
        player: MockPlayer = MockPlayer()
        player.get_player_choice_expedition_rewards_returns(
            lambda info_available_actions, info_expedition_level, info_turn_descriptor: ResultLookup(
                True,
                [info_available_actions[0],
                 info_available_actions[1],
                 PayAction({ResourceTypeEnum.wood: 2})]))
        return player

    def test_then_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_false(self) -> None:
        self.assertFalse(self._result.flag)

    def test_then_result_value_should_be_none(self) -> None:
        self.assertIsNone(self._result.value)

    def test_then_result_errors_should_not_be_empty(self) -> None:
        self.assertGreater(len(cast(List, self._result.errors)), 0)