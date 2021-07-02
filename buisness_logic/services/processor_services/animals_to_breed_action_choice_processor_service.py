from typing import NamedTuple, List, Tuple

from core.constants import resource_types
from core.enums.caverna_enums import ResourceTypeEnum
from core.services.base_action_choice_processor_service import BaseActionChoiceProcessorService


class AnimalsToBreedActionChoice(NamedTuple):
    hashcode: int
    animals_to_breed: List[ResourceTypeEnum]


class AnimalsToBreedActionChoiceProcessorService(BaseActionChoiceProcessorService):
    def __init__(self) -> None:
        self._threshold: float = 0.5

        BaseActionChoiceProcessorService.__init__(self, len(resource_types.farm_animals))

    def process_action_choice_for_animals_to_breed(
            self,
            maximum_number_of_animals) -> AnimalsToBreedActionChoice:
        action_reward_choices: List[float] = self._action_choice[
                                             self.offset:
                                             self.offset + self._length]
        probabilities: List[Tuple[int, float]] = [(index, probability) for
                                                  index, probability in enumerate(action_reward_choices)]
        probabilities = sorted(probabilities, key=lambda x: x[1], reverse=True)

        animals_to_breed: List[ResourceTypeEnum] = []
        hashcode: int = 0

        for index, probability in probabilities:
            if index in self._invalid_actions:
                continue
            should_purchase: bool = probability > self._threshold
            if should_purchase:
                item_to_purchase: ResourceTypeEnum = resource_types.farm_animals[index]
                animals_to_breed.append(item_to_purchase)
                hashcode <<= 2 + index
            else:
                # order is sorted by probability, so if we're below the threshold, nothing else will be valid
                break

        result: AnimalsToBreedActionChoice = AnimalsToBreedActionChoice(hashcode, animals_to_breed)
        return result

    def mark_invalid_action(
            self,
            hashcode: int) -> None:
        index: int = hashcode | 0b11
        self._invalid_actions.append(index)
