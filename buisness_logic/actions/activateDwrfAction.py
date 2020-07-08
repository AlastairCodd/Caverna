from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_action import BaseAction


class ActivateDwarfAction(BaseAction):
    def invoke(self, player: 'Player', active_card: 'BaseCard', current_dwarf: Dwarf) -> ResultLookup[int]:
        result: ResultLookup[int]
        if current_dwarf.is_active:
            result = ResultLookup(errors="Dwarf is already active")
        else:
            current_dwarf.set_active(active_card)
            result = ResultLookup(True, 1)
        return result

    def new_turn_reset(self):
        pass