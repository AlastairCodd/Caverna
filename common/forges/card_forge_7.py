from typing import List

from buisness_logic.cards import *
from common.forges.base_card_forge import BaseCardForge
from core.baseClasses.base_card import BaseCard


class SevenCardForge(BaseCardForge):
    def is_valid_for_number_of_players(self, number_of_players: int) -> bool:
        return number_of_players == 7

    def get_cards(self) -> List[BaseCard]:
        cards: List[BaseCard] = [
            depot_card.LargeDepotCard(),
            imitation_card.ImitationCard(0),
            extension_card.ExcensionCard()
        ]

        return cards
