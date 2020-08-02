from typing import List, Union

from buisness_logic.services.available_card_service import AvailableCardService
from buisness_logic.services.base_card_player_choice_transfer_service import BaseCardPlayerChoiceTransferService
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_card import BaseCard
from core.services.base_player_service import BasePlayerService


class CompleteCardPlayerChoiceTransferService(BaseCardPlayerChoiceTransferService):
    def __init__(self):
        self._available_card_service: AvailableCardService = AvailableCardService()

    def get_card(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[BaseCard]:
        if player is None:
            raise ValueError("Player cannot be null")
        if dwarf is None:
            raise ValueError("Dwarf cannot be null")

        success: bool = True
        chosen_card: Union[BaseCard, None] = None
        errors: List[str] = []

        card_choice_result: ResultLookup[BaseCard]

        available_cards: List[BaseCard] = self._available_card_service.get_cards_which_are_free_to_use(turn_descriptor.cards)
        card_choice_result = player.get_player_choice_card_to_use(
            available_cards,
            turn_descriptor)

        success &= card_choice_result.flag
        errors.extend(card_choice_result.errors)

        if card_choice_result.flag:
            chosen_card = card_choice_result.value

        result: ResultLookup[BaseCard] = ResultLookup(success, chosen_card, errors)
        return result
