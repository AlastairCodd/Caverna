from common.entities.weapon import Weapon


class Dwarf(object):
    def __init__(self, is_adult: bool = False):
        self._is_adult = is_adult
        self._weapon = None
        self._current_card = None

    def is_adult(self) -> bool:
        return self._is_adult

    def set_is_adult(self, is_adult: bool) -> bool:
        self._is_adult = is_adult
        return self._is_adult

    def give_weapon(self, weapon: Weapon):
        if self._weapon is not None:
            raise ValueError("dwarf already has a weapon")

        self._weapon = weapon

    @property
    def weapon(self) -> Weapon:
        return self._weapon

    def has_weapon(self) -> bool:
        result = self._weapon is None
        return result

    def set_active(self, current_card):
        if current_card is None:
            raise ValueError("current card must not be none")

        if self._current_card is not None:
            raise ValueError("already active")

        self._current_card = current_card

    def clear_active_card(self):
        self._current_card = None

    def is_active(self) -> bool:
        is_active = self._current_card is None
        return is_active
