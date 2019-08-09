from typing import Dict, Mapping
from common.entities.player import Player
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard


class PayAction(BaseAction):
    _payItems = Dict[ResourceTypeEnum, int]

    def __init__(self, payItems: Mapping[ResourceTypeEnum, int]):
        if payItems is None:
            raise ValueError("payItems")
        self._payItems = payItems

    def invoke(
            self,
            player: Player,
            activeCard: BaseCard) -> bool:
        if player is None:
            raise ValueError("player")

        raise NotImplementedError()
