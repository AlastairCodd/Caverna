from typing import Dict

from automated_tests.business_logic_tests.service_tests.processor_service_tests.card_action_choice_processor_service_tests.\
    given_a_card_action_choice_processor_service import Given_A_CardActionChoiceProcessorService
from core.constants import card_ids


class test_when_index_is_in_range(Given_A_CardActionChoiceProcessorService):
    def because(self) -> None:
        self._card_choices: Dict[int, int] = {
            1: card_ids.AdventureCardId,  # give dwarf weapon and go on expedition with next dwarf
            2: card_ids.AdventureCardId,  # go on an expedition with next dwarf
            3: card_ids.AdventureCardId,  # go on an expedition with dwarf 0
            4: card_ids.AdventureCardId,  # go on an expedition with dwarf 1
            5: card_ids.AdventureCardId,  # go on an expedition with dwarf 2
            6: card_ids.AdventureCardId,  # go on an expedition with dwarf 3
            7: card_ids.AdventureCardId,  # go on an expedition with dwarf 4
            8: card_ids.AdventureCardId,  # go on an expedition with dwarf 5

            9: card_ids.BlacksmithCardId,  # give dwarf weapon and go on expedition with next dwarf
            10: card_ids.BlacksmithCardId,  # go on an expedition with next dwarf
            11: card_ids.BlacksmithCardId,  # go on an expedition with dwarf 0
            12: card_ids.BlacksmithCardId,  # go on an expedition with dwarf 1
            13: card_ids.BlacksmithCardId,  # go on an expedition with dwarf 2
            14: card_ids.BlacksmithCardId,  # go on an expedition with dwarf 3
            15: card_ids.BlacksmithCardId,  # go on an expedition with dwarf 4
            16: card_ids.BlacksmithCardId,  # go on an expedition with dwarf 5

            17: card_ids.ClearingCardId,  # take accumulated items and place a meadow field twin
            18: card_ids.ClearingCardId,  # take accumulated items

            19: card_ids.DepotCardId,  # take accumulated items

            20: card_ids.DonkeyFarmingCardId,  # place a single and twin pasture and stable and take accumulated items
            21: card_ids.DonkeyFarmingCardId,  # place a single and twin pasture and take accumulated items
            22: card_ids.DonkeyFarmingCardId,  # place a single pasture and stable and take accumulated items
            23: card_ids.DonkeyFarmingCardId,  # place a twin pasture and stable and take accumulated items
            24: card_ids.DonkeyFarmingCardId,  # place a single pasture and take accumulated items
            25: card_ids.DonkeyFarmingCardId,  # place a twin pasture and take accumulated items
            26: card_ids.DonkeyFarmingCardId,  # place a stable and take accumulated items
            27: card_ids.DonkeyFarmingCardId,  # take accumulated items

            28: card_ids.DriftMining2CardId,  # take accumulate items and place a cavern tunnel twin
            29: card_ids.DriftMiningOneStoneCardId,  # take accumulate items and place a cavern tunnel twin
            30: card_ids.DriftMiningTwoStoneCardId,  # take accumulate items and place a cavern tunnel twin

            31: card_ids.ExcavationOneStoneCardId,  # take accumulate items and place a cavern tunnel twin
            32: card_ids.ExcavationOneStoneCardId,  # take accumulate items and place a cavern cavern twin
            33: card_ids.ExcavationTwoStoneCardId,  # take accumulate items and place a cavern tunnel twin
            34: card_ids.ExcavationTwoStoneCardId,  # take accumulate items and place a cavern cavern twin

            35: card_ids.ExplorationCardId,  # go on an expedition with next dwarf
            36: card_ids.ExplorationCardId,  # go on an expedition with dwarf 0
            37: card_ids.ExplorationCardId,  # go on an expedition with dwarf 1
            38: card_ids.ExplorationCardId,  # go on an expedition with dwarf 2
            39: card_ids.ExplorationCardId,  # go on an expedition with dwarf 3
            40: card_ids.ExplorationCardId,  # go on an expedition with dwarf 4
            41: card_ids.ExplorationCardId,  # go on an expedition with dwarf 5

            42: card_ids.ExtensionCardId,  # place a meadow field twin and receive 1 wood
            43: card_ids.ExtensionCardId,  # place a cavern tunnel twin and receive 1 stone

            44: card_ids.FamilyLifeCardId,  # get a baby dwarf
            45: card_ids.FamilyLifeCardId,  # sow
            46: card_ids.FamilyLifeCardId,  # get a baby dwarf and sow

            47: card_ids.FenceBuildingLargeCardId,  # take accumulated items and place a single and twin pasture
            48: card_ids.FenceBuildingLargeCardId,  # take accumulated items and place a single
            49: card_ids.FenceBuildingLargeCardId,  # take accumulated items and place a twin pasture
            50: card_ids.FenceBuildingLargeCardId,  # take accumulated items

            51: card_ids.FenceBuildingSmallCardId,  # take accumulated items and place a single and twin pasture
            52: card_ids.FenceBuildingSmallCardId,  # take accumulated items and place a single
            53: card_ids.FenceBuildingSmallCardId,  # take accumulated items and place a twin pasture
            54: card_ids.FenceBuildingSmallCardId,  # take accumulated items

            55: card_ids.ForestExplorationFoodCardId,  # take accumulated items and receive 1 food
            56: card_ids.ForestExplorationVegCardId,  # take accumulated items and receive 1 veg

            57: card_ids.GrowthCardId,  # receive items
            58: card_ids.GrowthCardId,  # get a baby dwarf
            59: card_ids.GrowthCardId,  # receive items and get a baby dwarf (requires effect, 1/5)

            60: card_ids.HardwareRentalLargeCardId,  # receive items and go on an expedition and sow with next dwarf
            61: card_ids.HardwareRentalLargeCardId,  # receive items and go on an expedition and sow with dwarf 0
            62: card_ids.HardwareRentalLargeCardId,  # receive items and go on an expedition and sow with dwarf 1
            63: card_ids.HardwareRentalLargeCardId,  # receive items and go on an expedition and sow with dwarf 2
            64: card_ids.HardwareRentalLargeCardId,  # receive items and go on an expedition and sow with dwarf 3
            65: card_ids.HardwareRentalLargeCardId,  # receive items and go on an expedition and sow with dwarf 4
            66: card_ids.HardwareRentalLargeCardId,  # receive items and go on an expedition and sow with dwarf 5
            67: card_ids.HardwareRentalLargeCardId,  # receive items and sow

            68: card_ids.HardwareRentalSmallCardId,  # go on an expedition with next dwarf and sow
            69: card_ids.HardwareRentalSmallCardId,  # go on an expedition with dwarf 0 and sow
            70: card_ids.HardwareRentalSmallCardId,  # go on an expedition with dwarf 1 and sow
            71: card_ids.HardwareRentalSmallCardId,  # go on an expedition with dwarf 2 and sow
            72: card_ids.HardwareRentalSmallCardId,  # go on an expedition with dwarf 3 and sow
            73: card_ids.HardwareRentalSmallCardId,  # go on an expedition with dwarf 4 and sow
            74: card_ids.HardwareRentalSmallCardId,  # go on an expedition with dwarf 5 and sow
            75: card_ids.HardwareRentalSmallCardId,  # sow

            76: card_ids.HouseworkCardId,  # receive dog and furnish cavern
            77: card_ids.HouseworkCardId,  # receive dog
            78: card_ids.HouseworkCardId,  # furnish cavern

            79: card_ids.LargeDepotCardId,  # take accumulated items

            80: card_ids.LoggingOneCardId,  # take accumulated items and go on an expedition with next dwarf
            81: card_ids.LoggingOneCardId,  # take accumulated items and go on an expedition with dwarf 1
            82: card_ids.LoggingOneCardId,  # take accumulated items and go on an expedition with dwarf 2
            83: card_ids.LoggingOneCardId,  # take accumulated items and go on an expedition with dwarf 3
            84: card_ids.LoggingOneCardId,  # take accumulated items and go on an expedition with dwarf 4
            85: card_ids.LoggingOneCardId,  # take accumulated items and go on an expedition with dwarf 5

            86: card_ids.LoggingThreeCardId,  # take accumulated items and go on an expedition with next dwarf
            87: card_ids.LoggingThreeCardId,  # take accumulated items and go on an expedition with dwarf 1
            88: card_ids.LoggingThreeCardId,  # take accumulated items and go on an expedition with dwarf 2
            89: card_ids.LoggingThreeCardId,  # take accumulated items and go on an expedition with dwarf 3
            90: card_ids.LoggingThreeCardId,  # take accumulated items and go on an expedition with dwarf 4
            91: card_ids.LoggingThreeCardId,  # take accumulated items and go on an expedition with dwarf 5

            92: card_ids.OreDeliveryCardId,  # take accumulated items

            93: card_ids.OreMineConstructionCardId,  # place an ore mine/deep tunnel twin and receive ore and go on an expedition with next dwarf
            94: card_ids.OreMineConstructionCardId,  # place an ore mine/deep tunnel twin and receive ore and go on an expedition with dwarf 0
            95: card_ids.OreMineConstructionCardId,  # place an ore mine/deep tunnel twin and receive ore and go on an expedition with dwarf 1
            96: card_ids.OreMineConstructionCardId,  # place an ore mine/deep tunnel twin and receive ore and go on an expedition with dwarf 2
            97: card_ids.OreMineConstructionCardId,  # place an ore mine/deep tunnel twin and receive ore and go on an expedition with dwarf 3
            98: card_ids.OreMineConstructionCardId,  # place an ore mine/deep tunnel twin and receive ore and go on an expedition with dwarf 4
            99: card_ids.OreMineConstructionCardId,  # place an ore mine/deep tunnel twin and receive ore and go on an expedition with dwarf 4
            100: card_ids.OreMineConstructionCardId,  # go on an expedition with next dwarf
            101: card_ids.OreMineConstructionCardId,  # go on an expedition with dwarf 0
            102: card_ids.OreMineConstructionCardId,  # go on an expedition with dwarf 1
            103: card_ids.OreMineConstructionCardId,  # go on an expedition with dwarf 2
            104: card_ids.OreMineConstructionCardId,  # go on an expedition with dwarf 3
            105: card_ids.OreMineConstructionCardId,  # go on an expedition with dwarf 4
            106: card_ids.OreMineConstructionCardId,  # go on an expedition with dwarf 4

            107: card_ids.OreMiningTwoCardId,  # take accumulated items and receive ore conditionally
            108: card_ids.OreMiningThreeCardId,  # take accumulated items and receive ore conditionally

            109: card_ids.OreTradingCardId,  # trade 3x
            110: card_ids.OreTradingCardId,  # trade 2x
            111: card_ids.OreTradingCardId,  # trade 1x

            112: card_ids.RubyDeliveryCardId,  # take accumulated items and receive rubies conditionally

            113: card_ids.RubyMineConstructionCardId,  # place ruby mine on tunnel
            114: card_ids.RubyMineConstructionCardId,  # place ruby mine on deep tunnel and receive ruby
            115: card_ids.RubyMineConstructionCardId,  # place ruby mine on tunnel and on deep tunnel and receive ruby

            116: card_ids.RubyMiningCardId,  # take accumulated items and receive rubies conditionally

            117: card_ids.SheepFarmingCardId,  # place a single and twin pasture and stable and take accumulated items
            118: card_ids.SheepFarmingCardId,  # place a single and twin pasture and take accumulated items
            119: card_ids.SheepFarmingCardId,  # place a single pasture and stable and take accumulated items
            120: card_ids.SheepFarmingCardId,  # place a twin pasture and stable and take accumulated items
            121: card_ids.SheepFarmingCardId,  # place a single pasture and take accumulated items
            122: card_ids.SheepFarmingCardId,  # place a twin pasture and take accumulated items
            123: card_ids.SheepFarmingCardId,  # place a stable and take accumulated items
            124: card_ids.SheepFarmingCardId,  # take accumulated items

            125: card_ids.SlashAndBurnCardId,  # place a meadow field twin and sow
            126: card_ids.SlashAndBurnCardId,  # sow

            127: card_ids.SmallScaleDriftMiningCardId,  # place a cavern tunnel twin and receive one stone
            128: card_ids.SmallScaleDriftMiningCardId,  # receive one stone

            129: card_ids.StartingPlayerOreCardId,  # take accumulated items and become starting player and receive ore
            130: card_ids.StartingPlayerRubyCardId,  # take accumulated items and become starting player and receive ruby

            131: card_ids.StripMiningCardId,  # take accumulated items and receive wood

            132: card_ids.SuppliesCardId,  # receive items

            133: card_ids.SustenanceGrainCardId,  # place a meadow field twin and take accumulated items and receive one grain
            134: card_ids.SustenanceGrainCardId,  # take accumulated items and receive one grain

            135: card_ids.SustenanceVegAndGrainCardId,  # place a meadow field twin and take accumulated items and receive one grain
            136: card_ids.SustenanceVegAndGrainCardId,  # take accumulated items and receive one grain

            137: card_ids.UrgentWishForChildrenCardId,  # furnish a dwelling and get a baby dwarf
            138: card_ids.UrgentWishForChildrenCardId,  # receive three coins
            139: card_ids.UrgentWishForChildrenCardId,  # furnish a dwelling and get a baby dwarf and receive three coins

            140: card_ids.WeeklyMarketCardId,  # receive item and spend resources at market

            141: card_ids.WishForChildrenCardId,  # get a baby dwarf
            142: card_ids.WishForChildrenCardId,  # furnish a dwelling
            143: card_ids.WishForChildrenCardId,  # furnish a dwelling and get a baby dwarf

            144: card_ids.WoodGatheringCardId,  # take accumulated items
        }

    def test_then_result_should_be_expected(self) -> None:
        for index, card_id in self._card_choices.items():
            with self.subTest(index=index):
                calculated_card: CardActionChoice = self.SUT.convert_index_to_card_id(index)
                self.assertEqual(card_id, calculated_card.card_id)
