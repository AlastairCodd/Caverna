from typing import Dict, List
from common.entities.player import Player
from core.baseClasses.base_effect import BaseEffect
from core.enums.caverna_enums import TileTypeEnum
from common.services.tileTwinDefault import TileTwinDefault

class BaseConversionEffect(BaseEffect):
    def Invoke(self, source: Dict[TileTypeEnum, List[TileTypeEnum]]) -> Dict[TileTypeEnum, List[TileTypeEnum]]:
        raise NotImplementedException("base board effect class")
    
class ChangeFoodConversionRate(BaseConversionEffect):
    """Changes the default food conversion rates
    
    Params:
        newConversions = Dict[ResourceTypeEnum, int]: 
        from ResourceTypeEnum to x amount of food """

    def __init__(self, newConversions):
        self._newConversion = newConversions
        
class Convert(BaseConversionEffect):
    def __init__(self, input, output):
        """Optional conversion. Pay input and get output
    
        Params:
            input = Dict[ResourceTypeEnum, int]:
            output =  Dict[ResourceTypeEnum, int]:
            number of each type to give"""
        self._input = input
        self._output = output

class ConvertProportional(BaseConversionEffect):
    def __init__(self, input, output, condition):
        """Optional conversion. Pay an input and get a variable output
    
        Params:
            input: any object"""
        self._input = input
        self._output = output
        self._condition = condition