from typing import List

from buisness_logic.cards import *
from common.forges.base_card_forge import BaseCardForge
from core.baseClasses.base_card import BaseCard


class OneToThreeCardForge(BaseCardForge):
    def is_valid_for_number_of_players(self, number_of_players: int) -> bool:
        return 1 <= number_of_players <= 3

    def get_cards(self) -> List[BaseCard]:
        cards: List[BaseCard] = [
            drift_mining_card.DriftMiningOneStoneCard(),
            excavation_card.ExcavationOneCard(),
            starting_player_card.StartingPlayerOreCard(),
            logging_card.LoggingOneCard(),
            supplies_card.SuppliesCard(),
            ore_mining_card.OreMiningTwoCard(),
            wood_gathering_card.WoodGatheringCard(),
            clearing_card.ClearingCard(1),
            sustenance_card.SustenanceGrainCard()
        ]
        return cards
