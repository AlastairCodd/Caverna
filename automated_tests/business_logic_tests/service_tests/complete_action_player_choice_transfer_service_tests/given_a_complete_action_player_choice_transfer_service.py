from abc import ABC
from typing import List, Callable
from unittest import TestCase

from buisness_logic.services.complete_action_player_choice_transfer_service import CompleteActionPlayerChoiceTransferService
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from core.services.base_player_service import BasePlayerService
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.enums.harvest_type_enum import HarvestTypeEnum


class Given_A_CompleteActionPlayerChoiceTransferService(TestCase, ABC):
    def setUp(self) -> None:
        self.SUT: CompleteActionPlayerChoiceTransferService = CompleteActionPlayerChoiceTransferService()
        self.because()

    def because(self) -> None:
        pass


class FakeCompoundAction(BasePlayerChoiceAction):
    def __init__(self) -> None:
        self._player_choice_additional_action_choices_func: Callable[
                [BasePlayerService,
                 Dwarf,
                 List[BaseCard],
                 int,
                 int,
                 HarvestTypeEnum],
                ResultLookup[ActionChoiceLookup]] = \
            lambda info_player, info_dwarf, info_cards, info_turn_index, info_round_index, info_harvest_type: ResultLookup(errors="Not Implemented")

    def set_player_choice(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            cards: List[BaseCard],
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) -> ResultLookup[ActionChoiceLookup]:
        return self._player_choice_additional_action_choices_func(
            player,
            dwarf,
            cards,
            turn_index,
            round_index,
            harvest_type)

    def set_player_choice_returns(
            self,
            func: Callable[
                [BasePlayerService,
                 Dwarf,
                 List[BaseCard],
                 int,
                 int,
                 HarvestTypeEnum],
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
