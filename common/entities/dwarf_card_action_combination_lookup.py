from typing import cast

from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from core.baseClasses.base_card import BaseCard


class DwarfCardActionCombinationLookup(object):
    def __init__(
            self,
            dwarf: Dwarf,
            card: BaseCard,
            actions: ActionChoiceLookup) -> None:
        self._dwarf: Dwarf = dwarf
        self._card: BaseCard = card
        self._actions: ActionChoiceLookup = actions

    @property
    def dwarf(self) -> Dwarf:
        return self._dwarf

    @property
    def card(self) -> BaseCard:
        return self._card

    @property
    def actions(self) -> ActionChoiceLookup:
        return self._actions

    def __eq__(self, other) -> bool:
        result: bool = isinstance(other, DwarfCardActionCombinationLookup)

        if result:
            cast_other: DwarfCardActionCombinationLookup = cast(DwarfCardActionCombinationLookup, other)
            if self is not other:
                dwarves_equal: bool = self._dwarf == cast_other.dwarf
                cards_equal: bool = self._card == cast_other.card
                actions_equal: bool = self._actions == cast_other.actions
                result = dwarves_equal and cards_equal and actions_equal

        return result

    def __str__(self) -> str:
        return f"dwarf: {self._dwarf.weapon_level}  card: {self._card.name}  actions: {self._actions}"
