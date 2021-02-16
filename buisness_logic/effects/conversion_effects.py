from abc import ABCMeta, abstractmethod
from typing import Dict, List, Callable
from core.baseClasses.base_effect import BaseEffect
from core.enums.caverna_enums import TileTypeEnum, ResourceTypeEnum


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

    def __str__(self):
        return f"ConvertEffect({self._input}, {self._output})"
