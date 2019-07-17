from typing import Dict
from Core.baseCard import BaseCard
from Core.caverna_enums import ResourceTypeEnum, ActionCombinationEnum
from Common.Entities.multicombination import Combination
from BuisnessLogic.Actions import *

class Imitation1Card(BaseCard):
    
    def __init__(self):
        self._name = "Imitation"
        self._id = 10
        self._level = -1
        self._actions = Combination(
            ActionCombinationEnum.AndThen,
            payAction.PayAction( {ResourceTypeEnum.food, 1} ),
            useAnotherCardAction.UseAnotherCardAction() )