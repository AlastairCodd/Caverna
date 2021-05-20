from typing import NamedTuple, List, Tuple, Dict

from core.baseClasses.base_tile import BaseTile
from core.constants import game_constants, tile_ids
from core.services.base_action_choice_processor_service import BaseActionChoiceProcessorService


class PlacementActionChoice(NamedTuple):
    index: int
    location: int


class SpecificTilePlacementActionChoiceProcessorService(BaseActionChoiceProcessorService):
    def __init__(self):
        self._tile_id_to_offset: Dict[int, int] = {
            tile_ids.CavernTileId: 0,
            tile_ids.TunnelTileId: 1,
            tile_ids.DeepTunnelTileId: 2,
            tile_ids.OreMineTileId: 3,
            tile_ids.RubyMineTileId: 4,

            tile_ids.MeadowTileId: 5,
            tile_ids.FieldTileId: 6,
            tile_ids.PastureTileId: 7,
            tile_ids.LargePastureTileId: 8,
        }
        BaseActionChoiceProcessorService.__init__(self, len(self._tile_id_to_offset) * game_constants.default_board_tile_count)

    def process_action_choice_placement_for_tile(
            self,
            tile: BaseTile) -> PlacementActionChoice:
        if len(self._action_choice) != self._length:
            raise ValueError("Must set action choice before processing")
        if tile.id not in self._tile_id_to_offset:
            raise IndexError("Tile position cannot be set using this processor service")
        tile_action_choice_offset: int = self._tile_id_to_offset[tile.id] * game_constants.default_board_tile_count
        tile_placement_choices: List[float] = self._action_choice[
                                              tile_action_choice_offset + self.offset:
                                              tile_action_choice_offset + self.offset + game_constants.default_board_tile_count]
        locations: List[Tuple[int, float]] = [(index + tile_action_choice_offset, tile_placement_choices[index]) for index in range(len(tile_placement_choices))]
        locations = sorted(locations, key=lambda x: x[1])
        for index, probability in locations:
            if index in self._invalid_actions:
                continue
            return self.convert_index_to_placement(index)
        raise IndexError("No valid choices")

    def convert_index_to_placement(self, index):
        location: int = index % game_constants.default_board_tile_count
        return PlacementActionChoice(index, location)
