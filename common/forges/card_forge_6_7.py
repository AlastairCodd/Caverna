from typing import List

from buisness_logic.cards import *
from common.forges.base_card_forge import BaseCardForge
from core.baseClasses.base_card import BaseCard


class SixToSevenCardForge(BaseCardForge):
    def is_valid_for_number_of_players(self, number_of_players: int) -> bool:
        return 6 <= number_of_players <= 7

    def get_cards(self) -> List[BaseCard]:
        cards: List[BaseCard] = [
            depot_card.DepotCard(),
            drift_mining_2_card.DriftMining2Card(),
            weekly_market_card.WeeklyMarketCard(),
            imitation_card.ImitationCard(1),
            hardware_rental_card.HardwareRentalLargeCard(),
            fence_building_card.FenceBuildingLargeCard()
        ]

        return cards
