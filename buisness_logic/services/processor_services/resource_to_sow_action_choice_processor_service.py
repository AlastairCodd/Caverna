from typing import List, Tuple, NamedTuple

from core.enums.caverna_enums import ResourceTypeEnum
from core.services.base_action_choice_processor_service import BaseActionChoiceProcessorService


class ResourcesToSowActionChoice(NamedTuple):
    index: int
    resources_to_sow: List[ResourceTypeEnum]


class ResourceToSowActionChoiceProcessorService(BaseActionChoiceProcessorService):
    def __init__(self):
        self._resources_to_sow: List[List[ResourceTypeEnum]] = [
            [ResourceTypeEnum.veg, ResourceTypeEnum.veg, ResourceTypeEnum.veg],
            [ResourceTypeEnum.veg, ResourceTypeEnum.veg, ResourceTypeEnum.grain],
            [ResourceTypeEnum.veg, ResourceTypeEnum.grain, ResourceTypeEnum.grain],
            [ResourceTypeEnum.grain, ResourceTypeEnum.grain, ResourceTypeEnum.grain],

            [ResourceTypeEnum.veg, ResourceTypeEnum.veg],
            [ResourceTypeEnum.veg, ResourceTypeEnum.grain],
            [ResourceTypeEnum.grain, ResourceTypeEnum.grain],

            [ResourceTypeEnum.veg],
            [ResourceTypeEnum.grain],

            [],
        ]

        BaseActionChoiceProcessorService.__init__(self, len(self._resources_to_sow))

    def process_action_choice_for_resources_to_sow(self) -> ResourcesToSowActionChoice:
        probabilities: List[Tuple[int, float]] = self._get_action_choice_subset(self.length)

        for index, probability in probabilities:
            if index in self._invalid_actions:
                continue
            result: ResourcesToSowActionChoice = ResourcesToSowActionChoice(index, self._resources_to_sow[index])
            return result
        raise IndexError("No valid choices")