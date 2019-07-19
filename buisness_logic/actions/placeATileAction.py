from common.entities.player import Player
from core.baseClasses.base_action import BaseAction
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from core.baseClasses.base_card import BaseCard

class PlaceATileAction(BaseAction):
    _tileType: TileTypeEnum
    
    def __init__(self, tileType: TileTypeEnum):
        self._tileType = tileType
    
    def invoke(
        self,
        player: Player,
        activeCard: BaseCard ) -> bool:
        if player is None:
            raise ValueException("player")
        
        raise NotImplementedError()