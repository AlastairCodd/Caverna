from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_action import BaseAction


class MockAction(BaseAction):
    def new_turn_reset(self):
        pass

    def invoke(self, player: 'Player', active_card: 'BaseCard', current_dwarf: Dwarf) -> ResultLookup[int]:
        pass