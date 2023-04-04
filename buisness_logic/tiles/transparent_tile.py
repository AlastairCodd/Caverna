from buisness_logic.effects.receive_on_covering_effect import ReceiveOnCoveringEffect
from common.entities.tile_entity import TileEntity
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum


class TransparentTile(BaseTile):
    def __init__(
            self,
            tile_entity: TileEntity,
            resource: ResourceTypeEnum,
            amount: int = 1):
        BaseTile.__init__(
            self,
            tile_entity.tile_type.name,
            -1,
            tile_entity.tile_type,
            effects=[ReceiveOnCoveringEffect({resource: amount})])
