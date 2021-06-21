from typing import Tuple, List, NamedTuple

from core.baseClasses.base_action import BaseAction
from core.services.base_action_choice_processor_service import BaseActionChoiceProcessorService


class ExpeditionRewardActionChoice(NamedTuple):
    indexes: List[int]
    rewards: List[BaseAction]


class ExpeditionRewardActionChoiceProcessorService(BaseActionChoiceProcessorService):
    def __init__(self) -> None:
        self._expedition_reward_levels: List[int] = [
            1,  # UpgradeAllWeaponsAction
            1,  # Receive 1 Wood
            1,  # Receive 1 Dog
            2,  # Receive 1 Grain
            2,  # Receive 1 Sheep
            3,  # Receive 1 Stone
            3,  # Receive 1 Donkey
            4,  # Receive 1 Veg
            4,  # Receive 1 Ore
            5,  # Receive 1 Boar
            6,  # Receive 1 Coin
            7,  # Furnish a Cavern
            8,  # Place a stable for free
            9,  # Place a single Tunnel
            9,  # Place a single Pasture for 1 wood
            10,  # Place a twin Pasture for 2 wood
            10,  # Receive 1 Cow
            11,  # Place a single Meadow
            11,  # Build a Dwelling for 2 wood and 2 stone
            12,  # Place a single field
            12,  # Sow
            14,  # Place a single Cavern
            14,  # Breed up to 2 animals
        ]

        self._number_of_expedition_rewards: int = len(self._expedition_reward_levels)
        BaseActionChoiceProcessorService.__init__(self, self._number_of_expedition_rewards)

    def mark_invalid_action(
            self,
            index: int) -> None:
        if index < 0 or index >= self._length:
            raise ValueError(f"Index must be between zero and {self._length}")
        if index in self._invalid_actions:
            raise ValueError("Index is already marked as invalid")
        if index > self._number_of_expedition_rewards:
            sub_index: int = index - self._number_of_expedition_rewards
            lowest_index_of_same_level_as_sub_index: int = self._get_lowest_index_for_reward_of_same_level(sub_index)

            lower_bound_on_invalid_actions: int = lowest_index_of_same_level_as_sub_index + self._number_of_expedition_rewards

            self._invalid_actions.extend(range(lower_bound_on_invalid_actions, self._number_of_expedition_rewards * 2))
        else:
            lowest_index_of_same_level_as_sub_index: int = self._get_lowest_index_for_reward_of_same_level(index)

            self._invalid_actions.extend(range(lowest_index_of_same_level_as_sub_index, self._number_of_expedition_rewards))

    def _get_lowest_index_for_reward_of_same_level(self, index: int) -> int:
        level: int = self._expedition_reward_levels[index]
        for i in range(index, index - 3, -1):  # three is known to be the maximum number of items of the same level
            if i >= 0:
                if self._expedition_reward_levels[i] == level:
                    index = i
                else:
                    break
            else:
                break
        return index

    def process_action_choice_placement_for_rewards(
            self,
            number_of_rewards: int,
            is_first_expedition: bool,
            possible_expedition_rewards: List[BaseAction]) -> ExpeditionRewardActionChoice:
        additional_offset: int = len(self._expedition_reward_levels) if not is_first_expedition else 0
        probabilities: List[Tuple[int, float]] = self._get_action_choice_subset(self._length, additional_offset)

        reward_indexes: List[int] = []
        rewards: List[BaseAction] = []

        for reward_index, probability in probabilities:
            actual_index: int = reward_index + additional_offset
            if actual_index in self._invalid_actions:
                continue
            reward_action: BaseAction = possible_expedition_rewards[reward_index]

            reward_indexes.append(actual_index)
            rewards.append(reward_action)

            if len(rewards) >= number_of_rewards:
                break
        if len(rewards) == 0:
            raise IndexError("No valid choices")

        return ExpeditionRewardActionChoice(reward_indexes, rewards)
