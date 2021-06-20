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

        BaseActionChoiceProcessorService.__init__(self, len(self._expedition_reward_levels))

    def process_action_choice_placement_for_rewards(
            self,
            number_of_rewards: int,
            is_first_expedition: bool,
            possible_expedition_rewards: List[BaseAction]) -> ExpeditionRewardActionChoice:
        additional_offset: int = len(self._expedition_reward_levels) if not is_first_expedition else 0
        action_reward_choices: List[float] = self._action_choice[self.offset + additional_offset:
                                                                 self.offset + additional_offset + self._length]
        locations: List[Tuple[int, float]] = [(index, probability) for
                                              index, probability in enumerate(action_reward_choices)]
        locations = sorted(locations, key=lambda x: x[1], reverse=True)

        reward_indexes: List[int] = []
        rewards: List[BaseAction] = []

        for reward_index, probability in locations:
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
