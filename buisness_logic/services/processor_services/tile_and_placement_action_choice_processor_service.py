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
        if len(self._action_choice) != self._length:
            raise ValueError("Must set action choice before processing")
        tile_placement_choices: List[float] = self._action_choice[self.offset: self.offset + self._length]
        choices_and_locations: List[Tuple[int, float]] = [(index, tile_placement_choices[index]) for index in range(self._length)]
        choices_and_locations = sorted(choices_and_locations, key=lambda x: x[1])
        for index, probability in choices_and_locations:
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
