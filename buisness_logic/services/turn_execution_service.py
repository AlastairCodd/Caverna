from typing import List, NamedTuple

from buisness_logic.services.available_dwarf_service import AvailableDwarfService
from buisness_logic.services.base_action_player_choice_transfer_service import BaseActionPlayerChoiceTransferService
from buisness_logic.services.base_card_player_choice_transfer_service import BaseCardPlayerChoiceTransferService
from buisness_logic.services.base_dwarf_player_choice_transfer_service import BaseDwarfPlayerChoiceTransferService
from buisness_logic.services.complete_card_player_choice_transfer_service import CompleteCardPlayerChoiceTransferService
from buisness_logic.services.complete_dwarf_player_choice_transfer_service import CompleteDwarfPlayerChoiceTransferService
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.dwarf_card_action_combination_lookup import DwarfCardActionCombinationLookup
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from common.services.action_invoke_service import ActionInvokeService
from core.baseClasses.base_card import BaseCard
from core.constants import game_constants
from core.enums.harvest_type_enum import HarvestTypeEnum


class ChosenDwarfCardActionCombinationAndEquivalentLookup(NamedTuple):
    choice: DwarfCardActionCombinationLookup
    equivalents: List[DwarfCardActionCombinationLookup]


class TurnExecutionService(object):
    def __init__(self):
        self._actionInvokeService: ActionInvokeService = ActionInvokeService()
        self._available_dwarf_service: AvailableDwarfService = AvailableDwarfService()
        self.number_of_rounds: int = game_constants.number_of_rounds
        self._dwarf_transfer_service: BaseDwarfPlayerChoiceTransferService = CompleteDwarfPlayerChoiceTransferService()
        self._card_transfer_service: BaseCardPlayerChoiceTransferService = CompleteCardPlayerChoiceTransferService()
        self._action_transfer_service: BaseActionPlayerChoiceTransferService = None

    def take_turn(
            self,
            player: Player,
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum,
            cards: List[BaseCard]) -> ResultLookup[ChosenDwarfCardActionCombinationAndEquivalentLookup]:
        if player is None:
            raise ValueError
        if turn_index >= len(player.dwarves):
            raise IndexError(f"Turn Index ({turn_index}) must be less than number of dwarves ({len(player.dwarves)})")
        if round_index >= self.number_of_rounds:
            raise IndexError(f"Maximum number of turns of ")

        success: bool = False
        combinations: List[DwarfCardActionCombinationLookup]
        errors: List[str] = []

        dwarf_result = self._dwarf_transfer_service.get_dwarf(
            player,
            cards,
            turn_index,
            round_index,
            harvest_type)

        chosen_dwarf: Dwarf = dwarf_result.value

        errors.extend(dwarf_result.errors)

        if dwarf_result.flag:
            card_result: ResultLookup[BaseCard] = self._card_transfer_service.get_card(
                player,
                chosen_dwarf,
                cards,
                turn_index,
                round_index,
                harvest_type)

            chosen_card: BaseCard = card_result.value

            errors.extend(card_result.errors)

            if card_result.flag:
                action_result: ResultLookup[ActionChoiceLookup] = self._action_transfer_service.get_action(
                    player,
                    chosen_dwarf,
                    chosen_card,
                    cards,
                    turn_index,
                    round_index,
                    harvest_type)

                errors.extend(action_result.errors)

                if action_result.flag:
                    success = True

                    combinations = [DwarfCardActionCombinationLookup(
                        chosen_dwarf,
                        chosen_card,
                        action_result.value
                    )]
                else:
                    combinations = self.get_possible_
            else:
                equivalent_card: List[BaseCard] = self.get_equivalent_invalid_cards(player, chosen_dwarf, chosen_card)

        else:
            equivalent_dwarves: List[Dwarf] = self.get_equivalent_invalid_dwarves(player, chosen_dwarf)
            dwarf: Dwarf
            for dwarf in equivalent_dwarves:
                card: BaseCard
                for card in cards:
                    for action_combination_lookup in card.

        result: ResultLookup[ChosenDwarfCardActionCombinationAndEquivalentLookup] = ResultLookup(success, combinations, errors)
        return result

    def get_equivalent_invalid_dwarves(self, player: Player, chosen_dwarf: Dwarf) -> List[Dwarf]:
        result: List[Dwarf]

        if chosen_dwarf.is_active:
            result = [dwarf for dwarf in player.dwarves if dwarf.is_active]
        else:
            result = [chosen_dwarf]

        return result
