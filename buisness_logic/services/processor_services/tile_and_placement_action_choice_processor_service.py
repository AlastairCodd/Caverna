from typing import Tuple, List, NamedTuple

from core.constants import tile_ids, game_constants
from core.services.base_action_choice_processor_service import BaseActionChoiceProcessorService


class TileAndPlacementActionChoice(NamedTuple):
    index: int
    location: int
    tile_id: int


class TileAndPlacementActionChoiceProcessorService(BaseActionChoiceProcessorService):
    def __init__(self):
        BaseActionChoiceProcessorService.__init__(self, game_constants.default_board_tile_count * tile_ids.total_number_of_tiles)

    def process_action_choice_tile_and_placement(self) -> TileAndPlacementActionChoice:
        probabilities: List[Tuple[int, float]] = self._get_action_choice_subset(
            self._length)

        for index, probability in probabilities:
            if index in self._invalid_actions:
                continue
            return self.convert_index_to_tile_and_placement(index)
        raise IndexError("No valid choices")

    def convert_index_to_tile_and_placement(
            self,
            index: int) -> TileAndPlacementActionChoice:
        location: int = index % game_constants.default_board_tile_count
        tile_id: int = index // game_constants.default_board_tile_count
        return TileAndPlacementActionChoice(index, location, tile_id)
