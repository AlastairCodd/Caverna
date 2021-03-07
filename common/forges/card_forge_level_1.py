from numpy import random
from typing import List

from buisness_logic.cards.blacksmith_card import BlacksmithCard
from buisness_logic.cards.ore_mine_construction_card import OreMineConstructionCard
from buisness_logic.cards.sheep_farming_card import SheepFarmingCard
from common.forges.base_card_forge import BaseLevelledCardForge
from core.baseClasses.base_card import BaseCard


class Level1CardForge(BaseLevelledCardForge):
    def get_sequential_cards(self) -> List[BaseCard]:
        cards: List[BaseCard] = [
            BlacksmithCard(),
            OreMineConstructionCard(),
            SheepFarmingCard()]

        random.shuffle(cards)

        return cards
