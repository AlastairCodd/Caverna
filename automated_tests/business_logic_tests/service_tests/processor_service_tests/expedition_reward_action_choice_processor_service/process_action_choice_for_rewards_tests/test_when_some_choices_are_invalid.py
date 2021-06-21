from typing import List, Optional

from automated_tests.business_logic_tests.service_tests.processor_service_tests.expedition_reward_action_choice_processor_service.given_an_expedition_reward_action_choice_processor_service import \
    Given_An_ExpeditionRewardActionChoiceProcessorService
from buisness_logic.actions.place_a_single_tile_action import PlaceASingleTileAction
from buisness_logic.actions.place_a_twin_tile_action import PlaceATwinTileAction
from buisness_logic.actions.receive_action import ReceiveAction
from buisness_logic.services.processor_services.expedition_reward_action_choice_processor_service import \
    ExpeditionRewardActionChoice
from core.baseClasses.base_action import BaseAction
from core.enums.caverna_enums import ResourceTypeEnum, TileTypeEnum


class test_when_some_choices_are_invalid(Given_An_ExpeditionRewardActionChoiceProcessorService):
    def because(self) -> None:
        number_of_possible_rewards: int = 23
        self._expedition_level: int = 3

        possible_actions: List[Optional[BaseAction]] = [None for _ in range(number_of_possible_rewards)]
        action_choice: List[float] = [0.0 for _ in range(2 * number_of_possible_rewards)]

        self._expected_indexes: List[int] = [6, 8, 14]
        self._expected_rewards: List[BaseAction] = [
            ReceiveAction({ResourceTypeEnum.donkey: 1}),
            PlaceATwinTileAction(TileTypeEnum.pastureTwin, {ResourceTypeEnum.wood: 2}),
            PlaceASingleTileAction(TileTypeEnum.cavern),
        ]

        chosen_action_weighting: float = 0.8
        invalid_action_weighting: float = 0.9
        out_of_range_action_weighting: float = 1.0

        for index, reward in zip(self._expected_indexes, self._expected_rewards):
            action_choice[index] = chosen_action_weighting
            possible_actions[index] = reward

        action_choice[17] = invalid_action_weighting
        action_choice[18] = invalid_action_weighting
        action_choice[21] = invalid_action_weighting

        action_choice[2 + number_of_possible_rewards] = out_of_range_action_weighting
        action_choice[16 + number_of_possible_rewards] = out_of_range_action_weighting
        action_choice[17 + number_of_possible_rewards] = out_of_range_action_weighting

        self.SUT.set_action_choice(action_choice)
        self.SUT.mark_invalid_action(18)  # should mark this and all higher?

        self._result: ExpeditionRewardActionChoice = self.SUT.process_action_choice_placement_for_rewards(
            self._expedition_level,
            True,
            possible_actions)

    def test_then_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_indexes_should_contain_expected_number_of_results(self) -> None:
        self.assertEqual(len(self._result.indexes), self._expedition_level)

    def test_then_result_should_contain_same_number_of_indexes_as_reward_actions(self) -> None:
        self.assertEqual(len(self._result.indexes), len(self._result.rewards))

    def test_then_result_indexes_should_contain_expected_indexes(self) -> None:
        for index in self._expected_indexes:
            with self.subTest(index=index):
                self.assertIn(index, self._result.indexes)

    def test_then_result_rewards_should_contain_expected_reward_actions(self) -> None:
        for reward_action in self._expected_rewards:
            with self.subTest(reward=reward_action):
                self.assertIn(reward_action, self._result.rewards)
