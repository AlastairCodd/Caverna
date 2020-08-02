from typing import Union

from buisness_logic.services.base_card_player_choice_transfer_service import BaseCardPlayerChoiceTransferService
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_card import BaseCard
from core.services.base_player_service import BasePlayerService


class TrivialCardPlayerChoiceTransferService(BaseCardPlayerChoiceTransferService):
    def get_card(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[BaseCard]:
        if turn_descriptor is None:
            raise ValueError("Turn descriptor may not be null.")
        chosen_card: Union[BaseCard, None] = None

        card: BaseCard
        for card in turn_descriptor.cards:
            if not card.is_active:
                chosen_card = card
                break

        success: bool = chosen_card is not None
        error: Union[None, str] = None if success else "No cards remain"

        result: ResultLookup[BaseCard] = ResultLookup(success, chosen_card, error)
        return result
