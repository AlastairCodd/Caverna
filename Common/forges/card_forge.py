from typing import List
from buisness_logic.cards import *
from core.baseClasses.base_card import BaseCard


class CardForge(object):

    def create_all_cards(self) -> List[BaseCard]:
        """Returns a list containing a single instance of all of the cards"""
        cards = [
            clearing_card.clearingCard(),
            depot_card.depotCard(),
            drift_mining_card.driftMiningCard(),
            drift_mining_2_card.driftMining2Card(),
            excavation_card.excavationCard(),
            fence_building_card.fenceBuildingCard(),
            forest_exploration_card.forestExplorationCard(),
            growth_card.growthCard(),
            hardware_rental_card.hardwareRentalCard(),
            housework_card.houseworkCard(),
            imitation_1_card.Imitation1Card(),
            # TODO: Create card
            imitation_2_card.Imitation2Card(),
            logging_card.loggingCard(),
            ore_mining_card.oreMiningCard(),
            # TODO: Create card
            ruby_mining_1_card.RubyMining1Card(),
            # TODO: Create card
            slash_and_burn_card.slashAndBurnCard(),
            starting_player_card.startingPlayerCard(),
            sustenance_card.sustenanceCard(),
            weekly_market_card.weeklyMarketCard(),
            blacksmith_card.blacksmithCard(),
            ore_mine_construction_card.oreMineConstructionCard(),
            sheep_farming_card.sheepFarmingCard(),
            donkey_farming_card.donkeyFarmingCard(),
            # TODO: Create card
            ruby_mine_construction_card.rubyMineConstructionCard(),
            # TODO: Create card
            urgent_wish_for_children_card.urgentWishForChildrenCard(),
            # TODO: Create card
            wish_for_children_card.wishForChildrenCard(),
            # TODO: Create card
            exploration_card.explorationCard(),
            # TODO: Create card
            family_life_card.familyLifeCard(),
            ore_delivery_card.oreDeliveryCard(),
            adventure_card.adventureCard(),
            ore_trading_card.oreTradingCard(),
            # TODO: Create card
            ruby_mining_2_card.RubyMining2Card()
        ]
        return cards
