from common.entities.dwarf import Dwarf
from core.baseClasses.base_action import BaseAction
from core.containers.resource_container import ResourceContainer


class MockBaseAction(BaseAction):
    def invoke(self, player, active_card: ResourceContainer, current_dwarf: Dwarf) -> bool:
        pass

    def new_turn_reset(self):
        pass
