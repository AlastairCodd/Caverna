from typing import List, Tuple

from core.enums.caverna_enums import ResourceTypeEnum
from core.services.base_action_choice_processor_service import BaseActionChoiceProcessorService


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

    def process_action_choice_for_resources_to_sow(self) -> List[ResourceTypeEnum]:
        probabilities: List[Tuple[int, float]] = self._get_action_choice_subset(self.length)

        for index, probability in probabilities:
            if index in self._invalid_actions:
                continue
            return self._resources_to_sow[index]
        raise IndexError("No valid choices")