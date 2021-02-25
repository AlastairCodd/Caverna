from typing import List

from buisness_logic.cards import *
from common.forges.base_card_forge import BaseCardForge
from core.baseClasses.base_card import BaseCard


class FiveCardForge(BaseCardForge):
    def is_valid_for_number_of_players(self, number_of_players: int) -> bool:
        return number_of_players == 5

    def get_cards(self) -> List[BaseCard]:
        cards: List[BaseCard] = [
            depot_card.DepotCard(),
            small_scale_drift_mining_card.SmallScaleDriftMiningCard(),
            weekly_market_card.WeeklyMarketCard(),
            imitation_card.ImitationCard(4),
            hardware_rental_card.HardwareRentalSmallCard(),
            fence_building_card.FenceBuildingSmallCard()
        ]

        return cards
