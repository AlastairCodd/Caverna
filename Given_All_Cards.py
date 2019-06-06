from typing import Dict
from Core.baseCard import BaseCard
from Core.cavernaEnums import ResourceTypeEnum, ActionCombinationEnum
from Core.resourceContainer import ResourceContainer
from Common.Entities.multiconditional import Conditional
from BuisnessLogic.Cards import *

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
		OreTradingCard.OreTradingCard()
		RubyMiningCard.RubyMiningCard()
		AdventureCard.AdventureCard()
		
if __name__ == "__main__":
	Given_All_Cards()