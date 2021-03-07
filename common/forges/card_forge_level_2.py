from numpy import random
from typing import List

from buisness_logic.cards.donkey_farming_card import DonkeyFarmingCard
from buisness_logic.cards.ruby_mine_construction_card import RubyMineConstructionCard
from buisness_logic.cards.wish_for_children_card import WishForChildrenCard, UrgentWishForChildrenCard
from common.forges.base_card_forge import BaseLevelledCardForge
from core.baseClasses.base_card import BaseCard


class Level2CardForge(BaseLevelledCardForge):
    def get_sequential_cards(self) -> List[BaseCard]:
        disordered_cards: List[BaseCard] = [
            RubyMineConstructionCard(),
            DonkeyFarmingCard()]

        random.shuffle(disordered_cards)

        cards: List[BaseCard] = [WishForChildrenCard()]
        cards.extend(disordered_cards)

        return cards

    def get_additional_cards(self) -> List[BaseCard]:
        return [UrgentWishForChildrenCard()]
