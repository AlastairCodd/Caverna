from typing import Dict, List
from common.entities.player import Player
from core.baseClasses.base_effect import BaseEffect
from core.enums.cavernaEnums import TileTypeEnum
from common.services.tileTwinDefault import TileTwinDefault

class BaseConversionEffect(BaseEffect):
	def Invoke(self, source: Dict[TileTypeEnum, List[TileTypeEnum]]) -> Dict[TileTypeEnum, List[TileTypeEnum]]:
		raise NotImplementedException("base board effect class")
	
class ChangeFoodConversionRate(BaseConversionEffect):
    '''Changes the default food conversion rates
    
    Params:
        newConversions = Dict[ResourceTypeEnum, int]: 
        from ResourceTypeEnum to x amount of food '''

	def __init__(self, newConversions):
        self._newConversion = newConversions
		
class Convert(BaseConversionEffect):
    '''Optional conversion. Pay input and get output
    
    Params:
        input = Dict[ResourceTypeEnum, int]:
        output =  Dict[ResourceTypeEnum, int]:
        number of each type to give'''

	def __init__(self, input, output):
        self._input = input
        self._output = output

class ConvertConditional(BaseConversionEffect):
    '''Optional conversion. Pay input and get some quantity of output
    
    Params:
        input = List[ResourceTypeEnum]: 