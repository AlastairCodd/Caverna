from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.repositories.base_player_repository import BasePlayerRepository


class ActivateDwarfAction(BaseAction):
    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        """Activates the current dwarf at the beginning of a turn.

        :param player: Unused.
        :param active_card: Unused.
        :param current_dwarf: The dwarf to be activated.
        :return: A result lookup indicating the success of the action. This will never be null.
        """
        result: ResultLookup[int]
        if current_dwarf.is_active:
            result = ResultLookup(errors="Dwarf is already active")
        else:
            current_dwarf.set_active(active_card)
            result = ResultLookup(True, 1)
        return result

    def new_turn_reset(self):
        pass
