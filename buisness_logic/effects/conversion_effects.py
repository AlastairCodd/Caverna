from typing import Dict, List
from core.baseClasses.base_effect import BaseEffect
from core.enums.caverna_enums import TileTypeEnum


class BaseConversionEffect(BaseEffect):
    def invoke(self, source: Dict[TileTypeEnum, List[TileTypeEnum]]) -> Dict[TileTypeEnum, List[TileTypeEnum]]:
        raise NotImplementedError("base board effect class")


class ChangeFoodConversionRate(BaseConversionEffect):
    """Changes the default food conversion rates
    
    Params:
        newConversions = Dict[ResourceTypeEnum, int]: 
        from ResourceTypeEnum to x amount of food """

    def __init__(self, new_conversion):
        BaseEffect.__init__(self)
        self._newConversion = new_conversion

    def invoke(self, source: Dict[TileTypeEnum, List[TileTypeEnum]]) -> Dict[TileTypeEnum, List[TileTypeEnum]]:
        raise NotImplementedError()


class Convert(BaseConversionEffect):
    def __init__(self, input, output):
        """Optional conversion. Pay input and get output

        Params:
            input = Dict[ResourceTypeEnum, int]:
            output =  Dict[ResourceTypeEnum, int]:
            number of each type to give"""
        BaseEffect.__init__(self)
        self._input = input
        self._output = output

    def invoke(self, source: Dict[TileTypeEnum, List[TileTypeEnum]]) -> Dict[TileTypeEnum, List[TileTypeEnum]]:
        pass


class ConvertProportional(BaseConversionEffect):
    def __init__(self, input, output, condition):
        """Optional conversion. Pay an input and get a variable output
    
        Params:
            input: any object"""
        BaseEffect.__init__(self)
        self._input = input
        self._output = output
        self._condition = condition

    def invoke(self, source: Dict[TileTypeEnum, List[TileTypeEnum]]) -> Dict[TileTypeEnum, List[TileTypeEnum]]:
        pass
