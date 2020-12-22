from abc import ABCMeta
from typing import Callable
from unittest import TestCase

from automated_tests.business_logic_tests.service_tests.complete_dwarf_player_choice_transfer_service_tests\
    .given_a_complete_dwarf_player_choice_transfer_service import FakeCard
from buisness_logic.services.complete_action_player_choice_transfer_service import CompleteActionPlayerChoiceTransferService
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.enums.harvest_type_enum import HarvestTypeEnum
from core.services.base_player_service import BasePlayerService


class Given_A_CompleteActionPlayerChoiceTransferService(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: CompleteActionPlayerChoiceTransferService = CompleteActionPlayerChoiceTransferService()
        self._turn_descriptor: TurnDescriptorLookup = TurnDescriptorLookup(
            [FakeCard()],
            [],
            0,
            0,
            HarvestTypeEnum.NoHarvest)

        self.because()

    def because(self) -> None:
        pass


class FakeCompoundAction(BasePlayerChoiceAction):
    def __init__(self) -> None:
        self._player_choice_additional_action_choices_func: Callable[
            [BasePlayerService,
             Dwarf,
             TurnDescriptorLookup],
            ResultLookup[ActionChoiceLookup]] = \
            lambda info_player, info_dwarf, info_turn_descriptor: ResultLookup(errors="Not Implemented")

    def set_player_choice(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        return self._player_choice_additional_action_choices_func(
            player,
            dwarf,
            turn_descriptor)

    def set_player_choice_returns(
            self,
            func: Callable[
                [BasePlayerService,
                 Dwarf,
                 TurnDescriptorLookup],
                ResultLookup[ActionChoiceLookup]]) -> None:
        self._player_choice_additional_action_choices_func = func

    def invoke(
            self,
            player: BasePlayerService,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        pass

    def new_turn_reset(self):
        pass
