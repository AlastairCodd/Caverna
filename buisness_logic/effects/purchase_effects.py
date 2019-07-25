from typing import Dict
from core.baseClasses.base_effect import BaseEffect
from core.enums.caverna_enums import ResourceTypeEnum
from common.defaults.tile_cost_default import TileCostDefault

class BasePurchaseEffect(BaseEffect):
    '''Abstract class for purchase effects'''
    
    def invoke(self):
        raise NotImplementedError()
    
class DecreasePrice(BasePurchaseEffect):
    def __init__(self, decreaseBy, subject):
        self._subject = subject
        self._decreaseBy = decreaseBy
    
    def invoke(self, target) -> Dict[ResourceTypeEnum, int]:
        '''Decrease the current price of target by self._decreaseBy
            to a minimum cost of 0
            
            Target: either a tileTypeEnum'''
        price = dict(target.get_price())
        for key in self._decreaseBy:
            currentPriceForKey = price.get(key, 0)
            targetPriceForKey = currentPriceForKey - self._decreaseBy[key]
            targetPriceForKey = max(0, targetPriceForKey)
            price[key] = targetPriceForKey
        return price
       
    def _get_cost(self, target) -> Dict[ResourceTypeEnum, int]:
        '''Get the default cost of the given target
        
        Target: either a tileTypeEnum, or an extension of BaseTile'''
        if target is None: raise ValueError("target")
                
        if issubclass(target, BaseTile):
            result = target.get_cost()
        elif isinstance(target, TileTypeEnum):
            costDefault = TileCostDefault()
            costs = costDefault.assign( {} )
            result = costs.getvalueordefault( target ) 