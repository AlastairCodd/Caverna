from typing import List

from buisness_logic.cards import strip_mining_card, imitation_card, forest_exploration_card
from common.forges.base_card_forge import BaseCardForge
from core.baseClasses.base_card import BaseCard


class ThreeCardForge(BaseCardForge):
    def is_valid_for_number_of_players(self, number_of_players: int) -> bool:
        return number_of_players == 3

    def get_cards(self) -> List[BaseCard]:
        cards: List[BaseCard] = [
            strip_mining_card.StripMiningCard(),
            imitation_card.ImitationCard(4),
            forest_exploration_card.ForestExplorationVegCard()
        ]

        return cards
