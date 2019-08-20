from core.baseClasses.base_action import BaseAction
from core.containers.resource_container import ResourceContainerard import BaseCard


class MockBaseAction(BaseAction):
    def new_turn_reset(self):
        pass

    def invoke(self, player, active_card: ResourceContainer) -> bool:
        pass