from typing import Dict
from core.baseClasses.base_effect import BaseEffect
from core.enums.caverna_enums import ResourceTypeEnum
from localised_resources.localiser import format_list_with_separator, format_resource_dict


class ConvertEffect(BaseEffect):
    def __init__(
            self,
            input_items: Dict[ResourceTypeEnum, int],
            output_items: Dict[ResourceTypeEnum, int]) -> None:
        """Optional conversion. Pay input and get output

        :param input_items:
        :param output_items:
        """
        self._input: Dict[ResourceTypeEnum, int] = input_items
        self._output: Dict[ResourceTypeEnum, int] = output_items

    @property
    def input(self) -> Dict[ResourceTypeEnum, int]:
        return self._input

    @property
    def output(self) -> Dict[ResourceTypeEnum, int]:
        return self._output

    def __str__(self) -> str:
        input_readable: str = format_resource_dict(self._input, " and ")
        output_readable: str = format_resource_dict(self._output, " and ")
        result: str = f"Allow conversion from {input_readable} to {output_readable}"
        return result

    def __repr__(self) -> str:
        return f"ConvertEffect({self._input}, {self._output})"
