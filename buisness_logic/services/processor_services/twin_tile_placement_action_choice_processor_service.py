from typing import NamedTuple, List, Tuple, Dict

from common.entities.tile_twin_placement_lookup import TileTwinPlacementLookup
from core.constants import game_constants
from core.enums.caverna_enums import TileTypeEnum, TileDirectionEnum
from core.services.base_action_choice_processor_service import BaseActionChoiceProcessorService


class PlacementActionChoice(NamedTuple):
    index: int
    placement: TileTwinPlacementLookup


class TwinTilePlacementActionChoiceProcessorService(BaseActionChoiceProcessorService):
    def __init__(self):
        self._tile_type_to_offset: Dict[TileTypeEnum, int] = {
            TileTypeEnum.meadowFieldTwin: 0,
            TileTypeEnum.cavernTunnelTwin: 1,
            TileTypeEnum.cavernCavernTwin: 2,
            TileTypeEnum.pastureTwin: 3,
            TileTypeEnum.oreMineDeepTunnelTwin: 4,
        }

        self._top_row_directions: List[TileDirectionEnum] = [
            TileDirectionEnum.right,
            TileDirectionEnum.down,
            TileDirectionEnum.left
        ]
        self._bottom_row_directions: List[TileDirectionEnum] = [
            TileDirectionEnum.up,
            TileDirectionEnum.right,
            TileDirectionEnum.left
        ]
        self._left_column_directions: List[TileDirectionEnum] = [
            TileDirectionEnum.up,
            TileDirectionEnum.right,
            TileDirectionEnum.down
        ]
        self._right_column_directions: List[TileDirectionEnum] = [
            TileDirectionEnum.up,
            TileDirectionEnum.down,
            TileDirectionEnum.left
        ]

        # (board count - edges * 4) + (perimeter - corners * 3) + (corners * 2)
        number_of_internal_tiles: int = (game_constants.default_board_width - 2) * (game_constants.default_board_height - 2)
        number_of_edge_tiles: int = (game_constants.default_board_width + game_constants.default_board_height) * 2 - 8
        number_of_corner_tiles: int = 4

        if number_of_internal_tiles + number_of_edge_tiles + number_of_corner_tiles != game_constants.default_board_tile_count:
            raise ValueError

        self._number_of_adjacent_tiles_for_edge_tile: int = 3

        self._total_number_of_tiles_adjacent_to_internal_tiles: int = number_of_internal_tiles * 4
        self._total_number_of_tiles_adjacent_to_edge_tiles: int = number_of_edge_tiles * self._number_of_adjacent_tiles_for_edge_tile
        self._total_number_of_tiles_adjacent_to_corner_tiles: int = number_of_corner_tiles * 2

        self._number_of_possible_twin_placements: int = self._total_number_of_tiles_adjacent_to_internal_tiles \
                                                        + self._total_number_of_tiles_adjacent_to_edge_tiles \
                                                        + self._total_number_of_tiles_adjacent_to_corner_tiles

        BaseActionChoiceProcessorService.__init__(self, len(self._tile_type_to_offset) * self._number_of_possible_twin_placements)

        top_left_corner_index: int = 0
        top_right_corner_index: int = game_constants.default_board_width - 1
        bottom_left_corner_index: int = (game_constants.default_board_height - 1) * game_constants.default_board_width
        bottom_right_corner_index: int = game_constants.default_board_tile_count - 1

        self._corner_directions: List[TileTwinPlacementLookup] = [
            TileTwinPlacementLookup(top_left_corner_index, TileDirectionEnum.right),
            TileTwinPlacementLookup(top_left_corner_index, TileDirectionEnum.down),
            TileTwinPlacementLookup(top_right_corner_index, TileDirectionEnum.down),
            TileTwinPlacementLookup(top_right_corner_index, TileDirectionEnum.left),
            TileTwinPlacementLookup(bottom_left_corner_index, TileDirectionEnum.up),
            TileTwinPlacementLookup(bottom_left_corner_index, TileDirectionEnum.right),
            TileTwinPlacementLookup(bottom_right_corner_index, TileDirectionEnum.up),
            TileTwinPlacementLookup(bottom_right_corner_index, TileDirectionEnum.left)]

    def process_action_choice_placement_for_tile(
            self,
            tile_type: TileTypeEnum) -> PlacementActionChoice:
        if tile_type not in self._tile_type_to_offset:
            raise IndexError("Tile position cannot be set using this processor service")
        tile_action_choice_offset: int = self._tile_type_to_offset[tile_type] * self._number_of_possible_twin_placements
        probabilities: List[Tuple[int, float]] = self._get_action_choice_subset(
            game_constants.default_board_tile_count,
            tile_action_choice_offset)

        for index, probability in probabilities:
            if index in self._invalid_actions:
                continue
            return self.convert_index_to_placement(index)
        raise IndexError("No valid choices")

    def convert_index_to_placement(self, index: int) -> PlacementActionChoice:
        local_index: int = index % self._number_of_possible_twin_placements
        placement: TileTwinPlacementLookup

        if local_index < self._total_number_of_tiles_adjacent_to_corner_tiles:
            placement = self._corner_directions[local_index]
        else:
            local_index -= self._total_number_of_tiles_adjacent_to_corner_tiles

            if local_index < self._total_number_of_tiles_adjacent_to_edge_tiles:
                number_of_placements_per_horizontal_edge_row: int = (game_constants.default_board_width - 2) * self._number_of_adjacent_tiles_for_edge_tile
                horizontal_cutoff: int = number_of_placements_per_horizontal_edge_row * 2

                if local_index < horizontal_cutoff:
                    location_offset: int
                    directions_by_index: List[TileDirectionEnum]
                    if local_index < number_of_placements_per_horizontal_edge_row:
                        location_offset = 1
                        directions_by_index = self._top_row_directions
                    else:
                        # bottom up, bottom right, bottom left (41-46)
                        location_offset = 41 - (game_constants.default_board_width - 2)
                        directions_by_index = self._bottom_row_directions

                    location: int = local_index // self._number_of_adjacent_tiles_for_edge_tile + location_offset
                    direction_index: int = local_index % self._number_of_adjacent_tiles_for_edge_tile

                    direction: TileDirectionEnum = directions_by_index[direction_index]

                    placement = TileTwinPlacementLookup(location, direction)
                else:
                    local_index -= horizontal_cutoff

                    number_of_placements_per_vertical_edge_row: int = (game_constants.default_board_height - 2) * self._number_of_adjacent_tiles_for_edge_tile

                    location: int
                    directions_by_index: List[TileDirectionEnum]
                    if local_index < number_of_placements_per_vertical_edge_row:
                        location = (local_index // self._number_of_adjacent_tiles_for_edge_tile + 1) * game_constants.default_board_width
                        directions_by_index = self._left_column_directions
                    else:
                        location = ((local_index - number_of_placements_per_vertical_edge_row) // self._number_of_adjacent_tiles_for_edge_tile + 2) \
                                   * game_constants.default_board_width - 1
                        directions_by_index = self._right_column_directions

                    direction_index: int = local_index % self._number_of_adjacent_tiles_for_edge_tile

                    direction: TileDirectionEnum = directions_by_index[direction_index]

                    placement = TileTwinPlacementLookup(location, direction)
            else:
                local_index -= self._total_number_of_tiles_adjacent_to_edge_tiles

                column_index: int = (local_index % 24) // 4
                row_index: int = local_index // 24

                location: int = 1 + column_index + ((row_index + 1) * game_constants.default_board_width)

                direction_index: int = local_index % 4
                direction: TileDirectionEnum = TileDirectionEnum(direction_index)

                placement = TileTwinPlacementLookup(location, direction)

        return PlacementActionChoice(index=index, placement=placement)
