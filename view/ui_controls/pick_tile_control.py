from typing import Iterable, Optional, List, Dict

from prompt_toolkit.buffer import Buffer
from prompt_toolkit.formatted_text import StyleAndTextTuples, to_formatted_text
from prompt_toolkit.key_binding import KeyBindings, KeyBindingsBase
from prompt_toolkit.layout import UIControl, UIContent
from prompt_toolkit.layout.controls import GetLinePrefixCallable
from prompt_toolkit.utils import Event

from buisness_logic.effects.allow_farming_effect import AllowFarmingEffect
from common.entities.tile_entity import TileEntity
from core.constants import game_constants
from core.containers.tile_container import TileContainer
from core.enums.caverna_enums import TileTypeEnum, ResourceTypeEnum
from localised_resources import user_interface_res


class PickTileControl(UIControl):
    def __init__(
            self,
            buffer: Optional[Buffer],
            use_compatible_characters: bool = False,
            show_tile_index: bool = True) -> None:
        self._tile_container: Optional[TileContainer] = None
        self._tile_container_changed_event: Event = Event(self)

        self._buffer: Optional[Buffer] = buffer

        self._use_compatible_characters: bool = use_compatible_characters
        self._show_tile_index: bool = show_tile_index

        self._key_bindings: KeyBindings = KeyBindings()
        self._key_bindings.add("c-m")(self.submit)
        self._key_bindings.add("right")(self.move_right)
        self._key_bindings.add("left")(self.move_left)
        self._key_bindings.add("down")(self.move_down)
        self._key_bindings.add("up")(self.move_up)

        self._box_content_width: int = 12
        self._box_content_height: int = 3

    def submit(self, _) -> None:
        if self._buffer is not None:
            self._buffer.insert_text("\nsubmit")

    def move_left(self, _) -> None:
        if self._buffer is not None:
            self._buffer.insert_text("\nmove left")

    def move_right(self, _) -> None:
        if self._buffer is not None:
            self._buffer.insert_text("\nmove right")

    def move_down(self, _) -> None:
        if self._buffer is not None:
            self._buffer.insert_text("\nmove down")

    def move_up(self, _) -> None:
        if self._buffer is not None:
            self._buffer.insert_text("\nmove up")

    def set_tile_container(self, tile_container: TileContainer) -> None:
        self._tile_container = tile_container
        self._tile_container_changed_event.fire()

    def is_focusable(self) -> bool:
        return True

    def preferred_width(self, max_available_width: int) -> Optional[int]:
        return game_constants.default_board_width * (self._box_content_width + 1) + 1

    def preferred_height(
            self,
            width: int,
            max_available_height: int,
            wrap_lines: bool,
            get_line_prefix: Optional[GetLinePrefixCallable]) -> Optional[int]:
        return game_constants.default_board_height * (self._box_content_height + 1) + 1

    def create_content(self, width: int, height: int) -> UIContent:
        if self._tile_container is None:
            result: UIContent = UIContent()
            return result

        lines: List[str] = []

        for row_index in range(self._tile_container.height):
            chunk: List[List[str]] = [["" for _ in range(self._tile_container.width)] for _ in range(self._box_content_height + 1)]

            for column_index in range(self._tile_container.width):
                tile_index: int = row_index * self._tile_container.width + column_index
                tile: TileEntity = self._tile_container.tiles[tile_index]

                chunk[0][column_index] = self._get_header(tile_index)
                tile_name: str

                tile_description_chunk: List[str]

                if tile.tile_type is TileTypeEnum.furnishedDwelling or tile.tile_type is TileTypeEnum.furnishedCavern:
                    tile_description_chunk = self._process_tile_name(tile.tile.name)
                else:
                    stored_resources: Dict[ResourceTypeEnum, int] = {}

                    effect: AllowFarmingEffect
                    for effect in tile.get_effects_of_type(AllowFarmingEffect):
                        if effect.planted_resource_amount > 0:
                            stored_resources.setdefault(effect.planted_resource_type, 0)
                            stored_resources[effect.planted_resource_type] += effect.planted_resource_amount

                    tile_description_chunk = self._process_tile_name(user_interface_res.tile_name_long[tile.tile_type])
                    name_length: int = len(tile_description_chunk)

                    if any(stored_resources):
                        item_description_lines: List[str] = [f"{amount} {resource.name}" for resource, amount in stored_resources.items()]
                        space_for_additional: int = self._box_content_height - name_length

                        for item_description_index, item_description_line in enumerate(item_description_lines):
                            if item_description_index >= space_for_additional:
                                break
                            tile_description_chunk.append(item_description_line)

                for index, description_chunk_line in enumerate(tile_description_chunk):
                    chunk[index + 1][column_index] = description_chunk_line

            for chunk_index, chunk_line in enumerate(chunk):
                new_line: str
                is_header: bool = chunk_index == 0
                separator_for_row: str = self._get_separator_for_row(row_index, not is_header)

                if is_header:
                    start_of_row: str = self._get_start_of_row(row_index)
                    end_of_row: str = self._get_end_of_row(row_index)
                    new_line = f"{start_of_row}{separator_for_row.join(chunk_line)}{end_of_row}"
                else:
                    line_without_ends: str = separator_for_row.join([f' {s.ljust(self._box_content_width - 1)}' for s in chunk_line])
                    new_line = f"{separator_for_row}{line_without_ends}{separator_for_row}"
                lines.append(new_line)

        separator_for_row: str = self._get_separator_for_row(self._tile_container.height, False)
        start_of_row: str = self._get_start_of_row(self._tile_container.height)
        end_of_row: str = self._get_end_of_row(self._tile_container.height)
        horizontal_separator: str = "-" if self._use_compatible_characters else "─"

        closing_line: str = f"{start_of_row}" \
                            f"{separator_for_row.join([horizontal_separator * self._box_content_width for _ in range(self._tile_container.width)])}" \
                            f"{end_of_row}"
        lines.append(closing_line)

        def get_line(i: int) -> StyleAndTextTuples:
            return to_formatted_text(lines[i], "")

        result: UIContent = UIContent(get_line=get_line, line_count=len(lines))
        return result

    def _process_tile_name(self, tile_name: str):
        name_parts: List[str] = tile_name.split()
        tile_description_chunk = [self._truncate(part)
                                  for part
                                  in (name_parts
                                      if len(name_parts) <= self._box_content_height
                                      else name_parts[:self._box_content_height])]
        return tile_description_chunk

    def _get_header(self, tile_index: int) -> str:
        vertical_separator: str = self._get_separator_for_row(0, True)
        horizontal_separator: str = "-" if self._use_compatible_characters else "─"
        result: str = f"{vertical_separator}{tile_index:0>2}{vertical_separator}{horizontal_separator * 2}" \
            .center(self._box_content_width, horizontal_separator) \
            if self._show_tile_index \
            else horizontal_separator * self._box_content_width
        return result

    def _truncate(self, part: str) -> str:
        return part if len(part) <= self._box_content_width - 2 else f"{part[:self._box_content_width - 5]}..."

    def _get_separator_for_row(
            self,
            row_index: int,
            is_header: bool) -> str:
        result: str
        if self._use_compatible_characters:
            result = "|"
        elif is_header:
            result = "│"
        else:
            result = "┬" if row_index == 0 else "┴" if row_index == self._tile_container.height else "┼"
        return result

    def _get_start_of_row(self, row_index: int) -> str:
        result: str
        if self._use_compatible_characters:
            result = "|"
        else:
            result = "┌" if row_index == 0 else "└" if row_index == self._tile_container.height else "├"
        return result

    def _get_end_of_row(self, row_index: int) -> str:
        result: str
        if self._use_compatible_characters:
            result = "|"
        else:
            result = "┐" if row_index == 0 else "┘" if row_index == self._tile_container.height else "┤"
        return result

    def get_invalidate_events(self) -> Iterable[Event[object]]:
        events: List[Event[object]] = [
            self._tile_container_changed_event
        ]
        return events

    def get_key_bindings(self) -> Optional[KeyBindingsBase]:
        return self._key_bindings

# "┌──|00|────┬──|01|────┬──|02|────┬──|03|────┬──|04|────┬──|05|────┬──|06|────┬──|07|────┐"
# "│ Field    │ Entry    │          │          │          │          │          │          │"
# "│ 2 Grain  │ Level    │          │          │          │          │          │          │"
# "│          │ Dwelling │          │          │          │          │          │          │"
# "├──|08|────┼──|09|────┼──|10|────┼──|11|────┼──|12|────┼──|13|────┼──|14|────┼──|15|────┤"
# "│          │          │          │          │          │          │          │          │"
# "│          │          │          │          │          │          │          │          │"
# "│          │          │          │          │          │          │          │          │"
# "├──|16|────┼──|17|────┼──|18|────┼──|19|────┼──|20|────┼──|21|────┼──|22|────┼──|23|────┤"
# "│          │          │          │          │          │          │          │          │"
# "│          │          │          │          │          │          │          │          │"
# "│          │          │          │          │          │          │          │          │"
# "├──|24|────┼──|25|────┼──|26|────┼──|27|────┼──|28|────┼──|29|────┼──|30|────┼──|31|────┤"
# "│          │          │          │          │          │          │          │          │"
# "│          │          │          │          │          │          │          │          │"
# "│          │          │          │          │          │          │          │          │"
# "├──|32|────┼──|33|────┼──|34|────┼──|35|────┼──|36|────┼──|37|────┼──|38|────┼──|39|────┤"
# "│          │          │          │          │          │          │          │          │"
# "│          │          │          │          │          │          │          │          │"
# "│          │          │          │          │          │          │          │          │"
# "├──|40|────┼──|41|────┼──|42|────┼──|43|────┼──|44|────┼──|45|────┼──|45|────┼──|47|────┤"
# "│          │          │          │          │          │          │          │          │"
# "│          │          │          │          │          │          │          │          │"
# "│          │          │          │          │          │          │          │          │"
# "└──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┘"
