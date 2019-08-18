from typing import Dict
from core.enums.caverna_enums import ResourceTypeEnum
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_action import BaseAction
from common.entities.player import Player


class ReceiveAction(BaseAction):
    def __init__(self, receive_items: Dict[ResourceTypeEnum, int]):
        if receive_items is None:
            raise ValueError("receiveItems")
        self._receiveItems: Dict[ResourceTypeEnum, int] = receive_items

    def invoke(
            self,
            player: Player,
            active_card: BaseCard) -> bool:
        if player is None:
            raise ValueError("player")

        return player.give_resources(self._receiveItems)

    def __str__(self) -> str:
        result = f"ReceiveAction({self._receiveItems})"
        return result
