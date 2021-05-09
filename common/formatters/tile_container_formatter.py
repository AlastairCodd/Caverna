import math
from typing import List, Tuple

from core.constants import html_tags
from core.containers.tile_container import TileContainer
from core.enums.caverna_enums import TileTypeEnum
from localised_resources import user_interface_res


class TileContainerFormatter(object):
    def format(
            self,
            tile_container: TileContainer,
            valid_locations: List[int]) -> str:
        index: int = 0
        tiles_map: List[Tuple[List[str], List[str]]] = []

        for y in range(tile_container.height):
            line_map_readable: List[str] = []
            line_map_number: List[str] = []
            for x in range(tile_container.width):
                tile_type_at_index: TileTypeEnum = tile_container.tiles[index].tile_type
                if (index % tile_container.width) == math.floor(tile_container.width / 2):
                    line_map_readable.append("|")
                    line_map_number.append("|")
                is_tile_type_unavailable: bool = tile_type_at_index is TileTypeEnum.unavailable
                is_location_valid: bool = index in valid_locations
                # is_location_valid = not is_tile_type_unavailable

                tile_value_readable: str
                tile_value_number: str

                if is_location_valid:
                    if (tile_type_at_index is TileTypeEnum.furnishedDwelling
                            or tile_type_at_index is TileTypeEnum.furnishedCavern):
                        tile_value_readable = tile_container.tiles[index].tile.name[0:2]
                    else:
                        tile_value_readable = user_interface_res.tile_name_short[tile_type_at_index]
                    tag: str = html_tags.tile_type_tags[tile_type_at_index]

                    tile_value_readable = f"<{tag}>{tile_value_readable.rjust(2)}</{tag}>"
                    tile_value_number = f"<{tag}>{str(index).rjust(2)}</{tag}>"
                elif not is_tile_type_unavailable:
                    tile_value_readable = " _"
                    tile_value_number = " _"
                else:
                    tile_value_readable = "  "
                    tile_value_number = "  "

                line_map_readable.append(tile_value_readable)
                line_map_number.append(tile_value_number)

                index += 1
            tiles_map.append((line_map_readable, line_map_number))

        result: str = ""
        for line_map_readable in tiles_map:
            result += f"{' '.join(line_map_readable[0])}    {' '.join(line_map_readable[1])}\n"

        return result
