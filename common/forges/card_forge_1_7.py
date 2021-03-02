from typing import List

from buisness_logic.cards import ruby_mining_card, housework_card, slash_and_burn_card
from common.forges.base_card_forge import BaseCardForge
from core.baseClasses.base_card import BaseCard


class OneToSevenCardForge(BaseCardForge):
    def is_valid_for_number_of_players(self, number_of_players: int) -> bool:
        return True

    def get_cards(self) -> List[BaseCard]:
        cards: List[BaseCard] = [
            ruby_mining_card.RubyMiningCard(),
            housework_card.HouseworkCard(),
            slash_and_burn_card.SlashAndBurnCard()
        ]

        return cards
