from common.entities.player import Player
from core.baseClasses.base_action import BaseAction
from core.containers.resource_container import ResourceContainer


class GoOnAnExpeditionAction(BaseAction):
    def __init__(self, level: int):
        if level < 1 or level > 4:
            raise ValueError("level")
        self._level = level

    def invoke(self, player: Player, active_card: ResourceContainer) -> bool:
        if player is None:
            raise ValueError("player")
        raise NotImplementedError

    def new_turn_reset(self):
        pass
