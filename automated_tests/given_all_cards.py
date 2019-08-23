from typing import Dict
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum
from core.containers.resource_container import ResourceContainer
from common.entities.multiconditional import Conditional
from buisness_logic.cards import *

class Given_All_Cards(object):
    
    def __init__(self):
        ClearingCard.ClearingCard()
        DepotCard.DepotCard()
        DriftMining2Card.DriftMining2Card()
        DriftMiningCard.DriftMiningCard()
        ExcavationCard.ExcavationCard()
        FenceBuildingCard.FenceBuildingCard()
        ForestExplorationCard.ForestExplorationCard()
        GrowthCard.GrowthCard()
        HardwareRentalCard.HardwareRentalCard()
        HouseworkCard.HouseworkCard()
        Imitation1Card.Imitation1Card()
        LoggingCard.LoggingCard()
        StartingPlayerCard.StartingPlayerCard()
        WeeklyMarketCard.WeeklyMarketCard()
        OreMineConstructionCard.OreMineConstructionCard()
        RubyMiningCard.RubyMiningCard()
        
if __name__ == "__main__":
    Given_All_Cards()