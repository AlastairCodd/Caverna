from typing import List, Tuple, NamedTuple

from core.enums.caverna_enums import ResourceTypeEnum
from core.services.base_action_choice_processor_service import BaseActionChoiceProcessorService


class MarketItemActionChoice(NamedTuple):
    hashcode: int
    items_to_purchase: List[ResourceTypeEnum]


class MarketItemsToPurchaseActionChoiceProcessorService(BaseActionChoiceProcessorService):
    def __init__(self) -> None:
        self._purchasable_items: List[ResourceTypeEnum] = [
            ResourceTypeEnum.dog,
            ResourceTypeEnum.sheep,
            ResourceTypeEnum.donkey,
            ResourceTypeEnum.boar,
            ResourceTypeEnum.cow,
            ResourceTypeEnum.wood,
            ResourceTypeEnum.stone,
            ResourceTypeEnum.ore,
            ResourceTypeEnum.grain,
            ResourceTypeEnum.veg,
        ]

        self._threshold: float = 0.5

        BaseActionChoiceProcessorService.__init__(self, len(self._purchasable_items))

    def process_action_choice_for_market_items(self) -> MarketItemActionChoice:
        action_reward_choices: List[float] = self._action_choice[
                                             self.offset:
                                             self.offset + self._length]
        probabilities: List[Tuple[int, float]] = [(index, probability) for
                                                  index, probability in enumerate(action_reward_choices)]
        probabilities = sorted(probabilities, key=lambda x: x[1], reverse=True)

        items_to_purchase: List[ResourceTypeEnum] = []
        hashcode: int = 0

        for index, probability in probabilities:
            if index in self._invalid_actions:
                continue
            should_purchase: bool = probability > self._threshold
            if should_purchase:
                item_to_purchase: ResourceTypeEnum = self._purchasable_items[index]
                items_to_purchase.append(item_to_purchase)
                hashcode = (11 * hashcode) + index + 1
            else:
                # order is sorted by probability, so if we're below the threshold, nothing else will be valid
                break

        result: MarketItemActionChoice = MarketItemActionChoice(hashcode, items_to_purchase)
        return result

    def mark_invalid_action(
            self,
            hashcode: int) -> None:
        index: int = hashcode % 11 - 1
        self._invalid_actions.append(index)
