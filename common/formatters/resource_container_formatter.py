from typing import Optional, Dict, List, Tuple

from core.constants import html_tags
from core.containers.resource_container import ResourceContainer
from core.enums.caverna_enums import ResourceTypeEnum


class ResourceContainerFormatter(object):
    def __init__(self,
                 number_of_rows: int = 5,
                 column_width: int = 20) -> None:
        self._number_of_rows: int = number_of_rows
        self._column_width: int = column_width

    def format(
            self,
            container: ResourceContainer,
            resource_delta: Optional[Dict[ResourceTypeEnum, int]] = None) -> str:
        if container is None:
            raise ValueError("Container may not be None")
        if resource_delta is None:
            resource_delta = {}

        max_name_length: int = -1

        for resource in ResourceTypeEnum:
            if resource == ResourceTypeEnum.begging_marker:
                continue
            name_length: int = len(resource.name)
            if name_length > max_name_length:
                max_name_length = name_length

        index: int = 0
        number_of_columns_in_row: List[int] = [0 for _ in range(self._number_of_rows)]
        number_of_control_bytes_in_row: List[int] = [0 for _ in range(self._number_of_rows)]
        resource_text: List[str] = ["" for _ in range(self._number_of_rows)]

        for resource in ResourceTypeEnum:
            if resource == ResourceTypeEnum.begging_marker:
                continue

            line: str = resource_text[index]
            line = line.ljust(self._column_width * number_of_columns_in_row[index] + number_of_control_bytes_in_row[index])

            new_line: str = f"{resource.name}:".ljust(max_name_length + 1)
            new_line += f" {str(container.get_resources_of_type(resource)).rjust(2)}"

            extra_amount: int = resource_delta.get(resource, 0)
            if extra_amount != 0:
                new_line += f"  <{html_tags.resource_delta}>({'+' if extra_amount > 0 else ''}{extra_amount})</{html_tags.resource_delta}>"
                number_of_control_bytes_in_row[index] += len(html_tags.resource_delta) * 2 + html_tags.open_close_tag_length

            resource_text[index] = line + new_line
            number_of_columns_in_row[index] += 1
            index += 1
            if index == self._number_of_rows:
                index = 0

        result: str = "\n".join(resource_text)
        return result
