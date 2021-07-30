from typing import List, Set, Tuple, Dict, NamedTuple

from core.enums.caverna_enums import ResourceTypeEnum
from core.services.base_action_choice_processor_service import BaseActionChoiceProcessorService


class ConversionsToPerformActionChoice(NamedTuple):
    hashcode: Tuple[int]
    conversions_to_perform: List[Tuple[Set[ResourceTypeEnum], int, Set[ResourceTypeEnum]]]


class ConversionsToPerformActionChoiceProcessorService(BaseActionChoiceProcessorService):
    def __init__(self) -> None:
        possible_conversions: List[Tuple[Dict[ResourceTypeEnum, int], Dict[ResourceTypeEnum, int]]] = [
            ({ResourceTypeEnum.ruby: 1}, {ResourceTypeEnum.dog: 1}),
            ({ResourceTypeEnum.ruby: 1}, {ResourceTypeEnum.grain: 1}),
            ({ResourceTypeEnum.ruby: 1}, {ResourceTypeEnum.veg: 1}),
            ({ResourceTypeEnum.ruby: 1}, {ResourceTypeEnum.sheep: 1}),
            ({ResourceTypeEnum.ruby: 1}, {ResourceTypeEnum.wood: 1}),
            ({ResourceTypeEnum.ruby: 1}, {ResourceTypeEnum.donkey: 1}),
            ({ResourceTypeEnum.ruby: 1}, {ResourceTypeEnum.stone: 1}),
            ({ResourceTypeEnum.ruby: 1}, {ResourceTypeEnum.boar: 1}),
            ({ResourceTypeEnum.ruby: 1}, {ResourceTypeEnum.ore: 1}),
            ({ResourceTypeEnum.ruby: 1, ResourceTypeEnum.food: 1}, {ResourceTypeEnum.cow: 1}),
            ({ResourceTypeEnum.coin: 2}, {ResourceTypeEnum.food: 1}),
            ({ResourceTypeEnum.coin: 3}, {ResourceTypeEnum.food: 2}),
            ({ResourceTypeEnum.coin: 4}, {ResourceTypeEnum.food: 3}),
            ({ResourceTypeEnum.donkey: 1}, {ResourceTypeEnum.food: 1}),
            ({ResourceTypeEnum.sheep: 1}, {ResourceTypeEnum.food: 1}),
            ({ResourceTypeEnum.grain: 1}, {ResourceTypeEnum.food: 1}),
            ({ResourceTypeEnum.boar: 1}, {ResourceTypeEnum.food: 2}),
            ({ResourceTypeEnum.veg: 1}, {ResourceTypeEnum.food: 2}),
            ({ResourceTypeEnum.ruby: 1}, {ResourceTypeEnum.food: 2}),
            ({ResourceTypeEnum.donkey: 2}, {ResourceTypeEnum.food: 3}),
            ({ResourceTypeEnum.cow: 1}, {ResourceTypeEnum.food: 3}),
            ({ResourceTypeEnum.coin: 2}, {ResourceTypeEnum.stone: 1, ResourceTypeEnum.wood: 1, ResourceTypeEnum.ore: 1}),
            ({ResourceTypeEnum.stone: 1, ResourceTypeEnum.wood: 1, ResourceTypeEnum.ore: 1}, {ResourceTypeEnum.coin: 2}),
            ({ResourceTypeEnum.boar: 2}, {ResourceTypeEnum.coin: 2, ResourceTypeEnum.food: 2}),
            ({ResourceTypeEnum.veg: 1, ResourceTypeEnum.grain: 1}, {ResourceTypeEnum.food: 5}),
            ({ResourceTypeEnum.ore: 1, ResourceTypeEnum.ruby: 1}, {ResourceTypeEnum.coin: 2, ResourceTypeEnum.food: 1}),
            ({ResourceTypeEnum.grain: 2}, {ResourceTypeEnum.food: 4}),
            ({ResourceTypeEnum.grain: 2}, {ResourceTypeEnum.coin: 3}),
        ]

        self._possible_conversions: List[Tuple[Set[ResourceTypeEnum], Set[ResourceTypeEnum]]] = []

        for conversion in possible_conversions:
            numberless_conversion: Tuple[Set[ResourceTypeEnum], Set[ResourceTypeEnum]] = (set(conversion[0].keys()), set(conversion[1].keys()))
            if numberless_conversion not in self._possible_conversions:
                self._possible_conversions.append(numberless_conversion)

        self._maximum_number_of_conversions_permitted: int = 5

        BaseActionChoiceProcessorService.__init__(self, len(self._possible_conversions) * self._maximum_number_of_conversions_permitted)

    def process_action_choice_conversions_to_perform(self) -> ConversionsToPerformActionChoice:
        hashcode: List[int] = []
        conversions_to_perform: List[Tuple[Set[ResourceTypeEnum], int, Set[ResourceTypeEnum]]] = []
        for conversion_index, possible_conversion in enumerate(self._possible_conversions):
            offset: int = conversion_index * self._maximum_number_of_conversions_permitted
            probabilities: List[Tuple[int, float]] = self._get_action_choice_subset(
                self._maximum_number_of_conversions_permitted,
                offset)

            for index_and_probability in probabilities:
                number_of_conversions_to_perform: int = index_and_probability[0]
                action_index: int = number_of_conversions_to_perform + offset

                if action_index in self._invalid_actions:
                    continue

                hashcode.append(action_index)

                if number_of_conversions_to_perform > 0:
                    conversions_to_perform.append((possible_conversion[0], number_of_conversions_to_perform, possible_conversion[1]))

        result: ConversionsToPerformActionChoice = ConversionsToPerformActionChoice(tuple(hashcode), conversions_to_perform)
        return result
