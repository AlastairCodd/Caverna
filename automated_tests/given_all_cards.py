from buisness_logic.cards import *


class Given_All_Cards(object):

    def __init__(self):
        clearing_card.ClearingCard()
        depot_card.DepotCard()
        drift_mining_2_card.DriftMining2Card()
        drift_mining_card.DriftMiningCard()
        excavation_card.ExcavationCard()
        fence_building_card.FenceBuildingCard()
        forest_exploration_card.ForestExplorationCard()
        growth_card.GrowthCard()
        hardware_rental_card.HardwareRentalCard()
        housework_card.HouseworkCard()
        imitation_1_card.Imitation1Card()
        logging_card.LoggingCard()
        starting_player_card.StartingPlayerCard()
        weekly_market_card.WeeklyMarketCard()
        ore_mine_construction_card.OreMineConstructionCard()
        ruby_mining_card.RubyMiningCard()


if __name__ == "__main__":
    Given_All_Cards()
