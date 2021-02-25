from typing import List

from buisness_logic.cards import *
from common.forges.base_card_forge import BaseCardForge
from core.baseClasses.base_card import BaseCard


class FourToSevenCardForge(BaseCardForge):
    def is_valid_for_number_of_players(self, number_of_players: int) -> bool:
        return 4 <= number_of_players <= 7

    def get_cards(self) -> List[BaseCard]:
        cards: List[BaseCard] = [
            drift_mining_card.DriftMiningTwoStoneCard(),
            excavation_card.ExcavationTwoCard(),
            starting_player_card.StartingPlayerRubyCard(),
            imitation_card.ImitationCard(2),
            logging_card.LoggingThreeCard(),
            growth_card.GrowthCard(),
            ore_mining_card.OreMiningTwoCard(),
            forest_exploration_card.ForestExplorationFoodCard(),
            clearing_card.ClearingCard(2),
            sustenance_card.SustenanceVegAndGrainCard()
        ]

        return cards
