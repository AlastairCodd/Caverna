from typing import Optional

from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.repositories.base_player_repository import BasePlayerRepository


class ActivateDwarfAction(BaseAction):
    def __init__(
            self,
            card_to_activate: Optional[BaseCard] = None) -> None:
        self._card_to_activate: Optional[BaseCard] = card_to_activate
        BaseAction.__init__(self, "ActivateDwarfAction")

    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        """Activates the current dwarf at the beginning of a turn.

        :param player: Unused.
        :param active_card: The card to apply the dwarf to. This will be used if no card was supplied in the ctor, and then cannot be None.
        :param current_dwarf: The dwarf to be activated.
        :return: A result lookup indicating the success of the action. This will never be null.
        """
        if self._card_to_activate is None and active_card is None:
            raise ValueError("Active Card may not be None if no card was provided in Ctor")
        if current_dwarf is None:
            raise ValueError("Dwarf may not be None")

        card_to_activate: BaseCard = active_card if self._card_to_activate is None else self._card_to_activate

        result: ResultLookup[int]
        if current_dwarf.is_active:
            result = ResultLookup(errors="Dwarf is already active")
        elif card_to_activate.is_active:
            result = ResultLookup(errors="Card is already active")
        else:
            current_dwarf.set_active(card_to_activate)
            card_to_activate.set_active()
            result = ResultLookup(True, 1)
        return result

    def new_turn_reset(self):
        # Probably not required, as action will go out of scope, but nice to have
        self._card_to_activate = None

    def __str__(self) -> str:
        return "Activate Dwarf Action"

    def __repr__(self) -> str:
        return "ActivateDwarfAction()"

    @property
    def card_to_activate(self) -> Optional[BaseCard]:
        return self._card_to_activate
