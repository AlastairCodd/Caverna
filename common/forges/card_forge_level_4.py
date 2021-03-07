from numpy import random
from typing import List

from buisness_logic.cards.adventure_card import AdventureCard
from buisness_logic.cards.ore_trading_card import OreTradingCard
from buisness_logic.cards.ruby_delivery_card import RubyDeliveryCard
from common.forges.base_card_forge import BaseLevelledCardForge
from core.baseClasses.base_card import BaseCard


class Level4CardForge(BaseLevelledCardForge):
    def get_sequential_cards(self) -> List[BaseCard]:
        cards: List[BaseCard] = [
            AdventureCard(),
            RubyDeliveryCard(),
            OreTradingCard()]

        random.shuffle(cards)

        return cards
