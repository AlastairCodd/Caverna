from abc import ABCMeta, abstractmethod
from typing import Dict, List, Callable
from core.baseClasses.base_effect import BaseEffect
from core.enums.caverna_enums import TileTypeEnum, ResourceTypeEnum


class BaseConversionEffect(BaseEffect, metaclass=ABCMeta):
    @abstractmethod
    def invoke(
            self,
            # TODO Change signature
            source: Dict[TileTypeEnum, List[TileTypeEnum]]) -> Dict[TileTypeEnum, List[TileTypeEnum]]:
        raise NotImplementedError("base board effect class")


class ChangeFoodConversionRate(BaseConversionEffect):
    def __init__(
            self,
            new_conversion: Dict[Dict[ResourceTypeEnum, int], int]) -> None:
        BaseEffect.__init__(self)
        self._newConversion: Dict[Dict[ResourceTypeEnum, int], int] = new_conversion

    def invoke(
            self,
            source: Dict[TileTypeEnum, List[TileTypeEnum]]) -> Dict[TileTypeEnum, List[TileTypeEnum]]:
        # TODO: Implement this
        raise NotImplementedError()


class Convert(BaseConversionEffect):
    def __init__(
            self,
            input_items: Dict[ResourceTypeEnum, int],
            output_items: Dict[ResourceTypeEnum, int]) -> None:
        """Optional conversion. Pay input and get output

        :param input_items:
        :param output_items:
        """
        BaseEffect.__init__(self)
        self._input: Dict[ResourceTypeEnum, int] = input_items
        self._output: Dict[ResourceTypeEnum, int] = output_items

    def invoke(
            self,
            source: Dict[TileTypeEnum, List[TileTypeEnum]]) -> Dict[TileTypeEnum, List[TileTypeEnum]]:
        # TODO: Implement this
        pass


class ConvertProportional(BaseConversionEffect):
    def __init__(
            self,
            input_items: Dict[ResourceTypeEnum, int],
            output_items: Dict[ResourceTypeEnum, int],
            # TODO: Change this type
            condition: Callable[[None], None]):
        """Optional conversion. Pay an input and get a variable output
    
        :param input_items:
        :param output_items:
        :param condition:
        """
        BaseEffect.__init__(self)
        self._input: Dict[ResourceTypeEnum, int] = input_items
        self._output: Dict[ResourceTypeEnum, int] = output_items
        self._condition: Callable[[None], None] = condition

    def invoke(
            self,
            source: Dict[TileTypeEnum, List[TileTypeEnum]]) -> Dict[TileTypeEnum, List[TileTypeEnum]]:
        # TODO: Implement this
        pass
