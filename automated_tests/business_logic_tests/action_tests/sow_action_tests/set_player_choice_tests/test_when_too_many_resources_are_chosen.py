from typing import cast

from automated_tests.business_logic_tests.action_tests.sow_action_tests.given_a_sow_action import Given_A_SowAction
from automated_tests.business_logic_tests.service_tests.complete_dwarf_player_choice_transfer_service_tests.given_a_complete_dwarf_player_choice_transfer_service import \
    FakeCard
from automated_tests.mocks.mock_player import MockPlayer
from buisness_logic.tiles.dwelling import Dwelling
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.enums.caverna_enums import ResourceTypeEnum
from core.enums.harvest_type_enum import HarvestTypeEnum
from core.services.base_player_service import BasePlayerService


class test_when_too_many_resources_are_chosen(Given_A_SowAction):
    def because(self) -> None:
        player: BasePlayerService = self._initialise_player()

        turn_descriptor: TurnDescriptorLookup = TurnDescriptorLookup(
            [FakeCard()],
            [Dwelling()],
            1,
            2,
            HarvestTypeEnum.Harvest)

        self._result: ResultLookup[ActionChoiceLookup] = self.SUT.set_player_choice(
            player,
            None,
            turn_descriptor
        )

    def _initialise_player(self) -> BasePlayerService:
        player: MockPlayer = MockPlayer()
        player.get_player_choice_resources_to_sow_returns(lambda x, _: ResultLookup(True, [ResourceTypeEnum.veg for _ in range(x + 1)]))
        return player

    def test_then_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_false(self) -> None:
        self.assertFalse(self._result.flag)

    def test_then_result_value_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result.value)

    def test_then_result_errors_should_not_be_empty(self) -> None:
        self.assertGreater(len(cast(list, self._result.errors)), 0)
