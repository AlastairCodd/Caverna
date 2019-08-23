from core.containers.resource_container import ResourceContainer
from core.baseClasses.base_action import BaseAction


class SowAction(BaseAction):

    def invoke(self, player: Player active_card: ResourceContainer) -> bool:
        if player is None:
            raise ValueError("player")
        raise NotImplementedError()

    def new_turn_reset(self):
        pass
