from numpy import random
from typing import List

from buisness_logic.cards.exploration_card import ExplorationCard
from buisness_logic.cards.family_life_card import FamilyLifeCard
from buisness_logic.cards.ore_delivery_card import OreDeliveryCard
from common.forges.base_card_forge import BaseLevelledCardForge
from core.baseClasses.base_card import BaseCard


class Level3CardForge(BaseLevelledCardForge):
    def get_sequential_cards(self) -> List[BaseCard]:
        cards: List[BaseCard] = [
            ExplorationCard(),
            OreDeliveryCard(),
            FamilyLifeCard()]

        random.shuffle(cards)

        return cards
