from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from common.entities.multicombination import Combination
from buisness_logic.actions import *

class OreMineConstructionCard(BaseCard):
    
    def __init__(self):
        self._name = "Ore Mine Construction"
        self._id = 22
        self._level = 1
        self._actions = Combination(
            ActionCombinationEnum.AndThenOr,
            Combination(
                ActionCombinationEnum.AndThen,
                placeATileAction.PlaceATileAction( TileTypeEnum.oreMineDeepTunnelTwin ),
                receiveAction.ReceiveAction( { ResourceTypeEnum.ore: 3 } ) ),
            goOnAnExpeditionAction.GoOnAnExpeditionAction( 3 ) )