from typing import Dict
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from core.containers.resource_container import ResourceContainer
from common.entities.multicombination import Combination
from buisness_logic.actions import *

class HouseworkCard(BaseCard):
    
    def __init__(self):
        self._name = "Housework"
        self._id = 8
        self._level = -1
        self._actions = Combination( 
            ActionCombinationEnum.AndOr,
            receiveAction.ReceiveAction( {ResourceTypeEnum.dog: 1} ),
            placeATileAction.PlaceATileAction( TileTypeEnum.furnishedCavern ) )