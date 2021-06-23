from typing import List

from automated_tests.business_logic_tests.service_tests.processor_service_tests.expedition_reward_action_choice_processor_service_tests.given_an_expedition_reward_action_choice_processor_service import \
    Given_An_ExpeditionRewardActionChoiceProcessorService


class test_when_called(Given_An_ExpeditionRewardActionChoiceProcessorService):
    def because(self) -> None:
        self._lowest_indexes: List[int] = [
            0,  # UpgradeAllWeaponsAction, Level 1
            0,  # Receive 1 Wood, Level 1
            0,  # Receive 1 Dog, Level 1
            3,  # Receive 1 Grain, Level 2
            3,  # Receive 1 Sheep, Level 2
            5,  # Receive 1 Stone, Level 3
            5,  # Receive 1 Donkey, Level 3
            7,  # Receive 1 Veg, Level 4
            7,  # Receive 1 Ore, Level 4
            9,  # Receive 1 Boar, Level 5
            10,  # Receive 1 Coin, Level 6
            11,  # Furnish a Cavern, Level 7
            12,  # Place a stable for free, Level 8
            13,  # Place a single Tunnel, Level 9
            13,  # Place a single Pasture for 1 wood, Level 9
            15,  # Place a twin Pasture for 2 wood, Level 10
            15,  # Receive 1 Cow, Level 10
            17,  # Place a single Meadow, Level 11
            17,  # Build a Dwelling for 2 wood and 2 stone, Level 11
            19,  # Place a single field, Level 12
            19,  # Sow, Level 12
            21,  # Place a single Cavern, Level 14
            21,  # Breed up to 2 animals, Level 14
        ]

    def test_then_result_should_be_expected(self) -> None:
        for index, expected_lowest_index in enumerate(self._lowest_indexes):
            with self.subTest(index=index):
                lowest_index: int = self.SUT._get_lowest_index_for_reward_of_same_level(index)
                self.assertEqual(lowest_index, expected_lowest_index)
