from typing import List, Union

from buisness_logic.services.base_card_player_choice_transfer_service import BaseCardPlayerChoiceTransferService
from common.entities.dwarf import Dwarf
from core.services.base_player_service import BasePlayerService
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.enums.harvest_type_enum import HarvestTypeEnum


class TrivialCardPlayerChoiceTransferService(BaseCardPlayerChoiceTransferService):
    def get_card(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            cards: List[BaseCard],
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) -> ResultLookup[BaseCard]:
        if cards is None:
            raise ValueError
        chosen_card: Union[BaseCard, None] = None

        card: BaseCard
        for card in cards:
            if not card.is_active:
                chosen_card = card
                break

        success: bool = chosen_card is not None
        error: Union[None, str] = None if success else "No cards remain"

        result: ResultLookup[BaseCard] = ResultLookup(success, chosen_card, error)
        return result
