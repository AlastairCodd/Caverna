from typing import List, Tuple

from common.entities.placement_action_choice import PlacementActionChoice
from core.constants import game_constants
from core.services.base_action_choice_processor_service import BaseActionChoiceProcessorService


class StablePlacementActionChoiceProcessorService(BaseActionChoiceProcessorService):
    def __init__(self) -> None:
        BaseActionChoiceProcessorService.__init__(self, game_constants.default_board_tile_count // 2)

    def process_action_choice_placement_for_stable(self) -> PlacementActionChoice:
        probabilities: List[Tuple[int, float]] = self._get_action_choice_subset(
            self._length)

        for index, probability in probabilities:
            if index in self._invalid_actions:
                continue
            return self.convert_index_to_placement(index)
        raise IndexError("No valid choices")

    def convert_index_to_placement(self, index) -> PlacementActionChoice:
        position: int = (index // 4) * 8 + index % 4
        return PlacementActionChoice(index, position)
