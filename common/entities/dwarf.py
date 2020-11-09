from typing import Union, Optional

from common.entities.result_lookup import ResultLookup
from common.entities.weapon import Weapon


class Dwarf(object):
    def __init__(self, is_adult: bool = False):
        self._is_adult: bool = is_adult
        self._weapon: Optional[Weapon] = None
        self._current_card: Optional['BaseCard'] = None

    @property
    def is_adult(self) -> bool:
        """Gets whether or not the dwarf is currently an adult.

        :return: True if the dwarf is an adult, false if not.
        """
        return self._is_adult

    @property
    def weapon(self) -> Union[Weapon, None]:
        """The weapon currently owned by the dwarf.

        :return: The weapon currently owned by the dwarf, if one exists. None if the dwarf does not have a weapon.
        """
        return self._weapon

    @property
    def has_weapon(self) -> bool:
        """Gets whether the dwarf has a weapon.

        :return: True if the dwarf has a weapon, false if not.
        """
        result: bool = self._weapon is not None
        return result

    @property
    def weapon_level(self) -> int:
        """Gets the strength of the dwarfs weapon.

        :return: The dwarf's weapon. 0 if the dwarf does not currently have a weapon.
        """
        weapon_level: int = 0 if self._weapon is None else self._weapon.level
        return weapon_level

    @property
    def is_active(self) -> bool:
        """Gets whether the dwarf is currently active.

        :return: True if the dwarf has been assigned to a card, false if not.
        """
        is_active: bool = self._current_card is not None
        return is_active

    @property
    def current_card_id(self) -> ResultLookup[int]:
        """Gets the id of the current card.

        :return: A result lookup, containing the id. Flag is false if the dwarf is not active.
        """
        result: ResultLookup[int]
        if self._current_card is None:
            result = ResultLookup(errors="Dwarf has not been assigned to a card")
        else:
            result = ResultLookup(True, self._current_card.id)
        return result

    def make_adult(self) -> ResultLookup[bool]:
        """Ages up child dwarves into adults.

        :return: A result lookup. Flag is true if the dwarf was previously a child and is now an adult, false if it was already an adult.
        """
        result: ResultLookup[bool]
        if self._is_adult:
            result = ResultLookup(False, False, errors="Dwarf is already an adult")
        else:
            self._is_adult = True
            result = ResultLookup(True, True)
        return result

    def give_weapon(self, weapon: Weapon) -> ResultLookup[int]:
        """Gives the dwarf the provided weapon.

        :param weapon: A weapon of any level. This cannot be none.
        :return: A result lookup. Flag is true if the dwarf has been given the weapon, false if it already has one. Value is the level of the new weapon,
            None if dwarf already has one.
        """
        if weapon is None:
            raise ValueError("Weapon cannot be none")

        result: ResultLookup[int]
        if self._weapon is not None:
            result = ResultLookup(errors="Dwarf already has a weapon")
        else:
            self._weapon = weapon
            result = ResultLookup(True, weapon.level)
        return result

    def set_active(
            self,
            new_card: 'BaseCard') -> ResultLookup['BaseCard']:
        """Activates the dwarf by placing it on the provided card.

        :param new_card: The new card the dwarf is being placed on. This cannot be none.
        :return: A result lookup. Flag indicates whether the dwarf was successfully placed; false if already active.
        """
        if new_card is None:
            raise ValueError("current card must not be none")

        result: ResultLookup['BaseCard']
        if self._current_card is not None:
            result = ResultLookup(errors="Dwarf is already active")
        else:
            self._current_card = new_card
            result = ResultLookup(True, new_card)
        return result

    def clear_active_card(self) -> ResultLookup['BaseCard']:
        """Clears the current active card from the dwarf.

        :return: A result lookup. Flag is always true. Value is either none, if the dwarf is already inactive, or the previous card.
        """
        result: ResultLookup['BaseCard']
        if self._current_card is None:
            result = ResultLookup(True, errors="Dwarf is already inactive")
        else:
            result = ResultLookup(True, self._current_card)
        self._current_card = None
        return result
