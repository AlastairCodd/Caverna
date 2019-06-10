from Core.resourceContainer import ActiveResourceContainer
from Common.Entities.multicombination import Combination
from BuisnessLogic.Cards import *

class Given_All_Cards(object):
	
	def __init__(self):
		self._cards = [
			ClearingCard.ClearingCard(),
			DepotCard.DepotCard(),
			DriftMining2Card.DriftMining2Card(),
			DriftMiningCard.DriftMiningCard(),
			ExcavationCard.ExcavationCard(),
			FenceBuildingCard.FenceBuildingCard(),
			ForestExplorationCard.ForestExplorationCard(),
			GrowthCard.GrowthCard(),
			HardwareRentalCard.HardwareRentalCard(),
			HouseworkCard.HouseworkCard(),
			Imitation1Card.Imitation1Card(),
			LoggingCard.LoggingCard(),
			OreMiningCard.OreMiningCard(),
			SmallScaleDriftMiningCard.SmallScaleDriftMiningCard(),
			StartingPlayerCard.StartingPlayerCard(),
			SuppliesCard.SuppliesCard(),
			SustenanceCard.SustenanceCard(),
			WeeklyMarketCard.WeeklyMarketCard(),
			BlacksmithCard.BlacksmithCard(),
			OreMineConstructionCard.OreMineConstructionCard(),
			SheepFarmingCard.SheepFarmingCard(),
			DonkeyFarmingCard.DonkeyFarmingCard(),
			OreDeliveryCard.OreDeliveryCard(),
			AdventureCard.AdventureCard(),
			RubyMiningCard.RubyMiningCard() ]
		
		print(len(self._cards))
		self.checkRefillActions()
		
	def checkRefillActions(self):
		activeResourceCards = [x for x in self._cards if issubclass(type(x), ActiveResourceContainer)]
		print(len(activeResourceCards))
		for card in activeResourceCards:
			print(f'{card._name}:')
			print(card.RefillAction())
			print(card.RefillAction())
			print()
		
if __name__ == "__main__":
	Given_All_Cards()