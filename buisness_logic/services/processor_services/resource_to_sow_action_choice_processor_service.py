from typing import List, Tuple, NamedTuple

from common.entities.resources_to_sow_lookup import ResourcesToSow
from core.enums.caverna_enums import ResourceTypeEnum
from core.services.base_action_choice_processor_service import BaseActionChoiceProcessorService


class ResourcesToSowActionChoice(NamedTuple):
    index: int
    resources_to_sow: ResourcesToSow


class ResourceToSowActionChoiceProcessorService(BaseActionChoiceProcessorService):
    def __init__(self):
        self._resources_to_sow: List[ResourcesToSow] = [
            ResourcesToSow(2, 2),
            ResourcesToSow(2, 1),
            ResourcesToSow(2, 0),
            ResourcesToSow(1, 2),
            ResourcesToSow(1, 1),
            ResourcesToSow(1, 0),
            ResourcesToSow(0, 2),
            ResourcesToSow(0, 1),
            ResourcesToSow(0, 0),
        ]

        BaseActionChoiceProcessorService.__init__(self, len(self._resources_to_sow))

    def process_action_choice_for_resources_to_sow(self) -> ResourcesToSowActionChoice:
        probabilities: List[Tuple[int, float]] = self._get_action_choice_subset(self.length)

        for index, probability in probabilities:
            if index in self._invalid_actions:
                continue
            result: ResourcesToSowActionChoice = ResourceToSowActionChoice(index, self._resources_to_sow[index])
            return result
        raise IndexError("No valid choices")
