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
        return self.__format__(0)

    def __format__(self, format_spec) -> str:
        newline_separator = " "
        try:
            num_spaces = int(format_spec)
            if num_spaces != 0:
                newline_separator = "\r\n" + " " * num_spaces
        except ValueError:
             pass

        result = "" if format_spec is None else f"Chosen Dwarf/Card/Action Combination{newline_separator}"
        result += f"dwarf with weapon: {self._dwarf.weapon_level}"
        result += f"{newline_separator}card: {self._card.name}"
        result += f"{newline_separator}actions: {self._actions}"
        return result
