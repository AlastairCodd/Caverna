from typing import Dict
from core.baseClasses.base_action import BaseAction
from core.enums.caverna_enums import ResourceTypeEnum


class UseAnotherCardAction(BaseAction):

    def invoke(self, player: Player active_card: Dict[ResourceTypeEnum, int]) -> bool:
        if player is None:
            raise ValueError("player")
        raise NotImplementedError

    def new_turn_reset(self):
        pass
