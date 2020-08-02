from typing import List, NamedTuple, Union

from buisness_logic.services.base_action_player_choice_transfer_service import BaseActionPlayerChoiceTransferService
from buisness_logic.services.base_card_player_choice_transfer_service import BaseCardPlayerChoiceTransferService
from buisness_logic.services.base_dwarf_player_choice_transfer_service import BaseDwarfPlayerChoiceTransferService
from buisness_logic.services.complete_action_player_choice_transfer_service import CompleteActionPlayerChoiceTransferService
from buisness_logic.services.complete_card_player_choice_transfer_service import CompleteCardPlayerChoiceTransferService
from buisness_logic.services.complete_dwarf_player_choice_transfer_service import CompleteDwarfPlayerChoiceTransferService
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.dwarf_card_action_combination_lookup import DwarfCardActionCombinationLookup
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from common.services.conditional_service import ConditionalService
from core.baseClasses.base_card import BaseCard
from core.services.base_player_service import BasePlayerService


class ChosenDwarfCardActionCombinationAndEquivalentLookup(NamedTuple):
    choice: Union[DwarfCardActionCombinationLookup, None]
    equivalents: List[DwarfCardActionCombinationLookup]


class TurnExecutionService(object):
    def __init__(self):
        self._conditional_service: ConditionalService = ConditionalService()

        self._dwarf_transfer_service: BaseDwarfPlayerChoiceTransferService = CompleteDwarfPlayerChoiceTransferService()
        self._card_transfer_service: BaseCardPlayerChoiceTransferService = CompleteCardPlayerChoiceTransferService()
        self._action_transfer_service: BaseActionPlayerChoiceTransferService = CompleteActionPlayerChoiceTransferService()

    def take_turn(
            self,
            player: BasePlayerService,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ChosenDwarfCardActionCombinationAndEquivalentLookup]:
        if player is None:
            raise ValueError("Player may not be null.")
        if turn_descriptor is None:
            raise ValueError("Turn descriptor may not be null.")
        if turn_descriptor.turn_index >= len(player.dwarves):
            raise IndexError(f"Turn Index ({turn_descriptor.turn_index}) must be less than number of dwarves ({len(player.dwarves)})")

        success: bool = False
        choice: Union[DwarfCardActionCombinationLookup, None] = None
        equivalents: List[DwarfCardActionCombinationLookup] = []
        errors: List[str] = []

        dwarf_result = self._dwarf_transfer_service \
            .get_dwarf(
                player,
                turn_descriptor)

        chosen_dwarf: Dwarf = dwarf_result.value

        errors.extend(dwarf_result.errors)

        if dwarf_result.flag:
            card_result: ResultLookup[BaseCard] = self._card_transfer_service \
                .get_card(
                    player,
                    chosen_dwarf,
                    turn_descriptor)

            chosen_card: BaseCard = card_result.value

            errors.extend(card_result.errors)

            if card_result.flag:
                action_result: ResultLookup[ActionChoiceLookup] = self._action_transfer_service \
                    .get_action(
                        player,
                        chosen_dwarf,
                        chosen_card,
                        turn_descriptor)

                errors.extend(action_result.errors)

                choice = DwarfCardActionCombinationLookup(
                    chosen_dwarf,
                    chosen_card,
                    action_result.value)

                if action_result.flag:
                    success = True
            else:
                equivalent_cards: List[BaseCard] = self.get_equivalent_invalid_cards(player, chosen_dwarf, chosen_card)
                card: BaseCard
                for card in equivalent_cards:
                    possible_choices: List[ActionChoiceLookup] = self._conditional_service.get_possible_choices(card.actions)
                    action_choice: ActionChoiceLookup
                    for action_choice in possible_choices:
                        new_equivalent: DwarfCardActionCombinationLookup = DwarfCardActionCombinationLookup(
                            chosen_dwarf,
                            card,
                            action_choice)
                        equivalents.append(new_equivalent)
        else:
            equivalent_dwarves: List[Dwarf] = self.get_equivalent_invalid_dwarves(player, chosen_dwarf)
            dwarf: Dwarf
            for dwarf in equivalent_dwarves:
                card: BaseCard
                for card in turn_descriptor.cards:
                    possible_choices: List[ActionChoiceLookup] = self._conditional_service.get_possible_choices(card.actions)
                    action_choice: ActionChoiceLookup
                    for action_choice in possible_choices:
                        new_equivalent: DwarfCardActionCombinationLookup = DwarfCardActionCombinationLookup(
                            dwarf,
                            card,
                            action_choice)
                        equivalents.append(new_equivalent)

        result: ResultLookup[ChosenDwarfCardActionCombinationAndEquivalentLookup]
        data: ChosenDwarfCardActionCombinationAndEquivalentLookup
        data = ChosenDwarfCardActionCombinationAndEquivalentLookup(
            choice,
            equivalents)
        result = ResultLookup(success, data, errors)
        return result

    def get_equivalent_invalid_dwarves(
            self,
            player: BasePlayerService,
            chosen_dwarf: Dwarf) -> List[Dwarf]:
        result: List[Dwarf]

        if chosen_dwarf.is_active:
            result = [dwarf for dwarf in player.dwarves if dwarf.is_active]
        else:
            result = [chosen_dwarf]

        return result

    def get_equivalent_invalid_cards(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            card: BaseCard) -> List[BaseCard]:
        # TODO: Implement this
        return []
