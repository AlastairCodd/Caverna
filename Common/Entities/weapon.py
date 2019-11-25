from common.entities.result_lookup import ResultLookup
from core.constants import weapon_constants


class Weapon(object):
    def __init__(self, level: int = 1):
        if level < weapon_constants.WeakestForgeableWeapon or level > weapon_constants.StrongestForgeableWeapon:
            raise ValueError(f"level at creation must be between {weapon_constants.WeakestForgeableWeapon} and {weapon_constants.StrongestForgeableWeapon}")
        self._level: int = level

    def increase_level(self) -> ResultLookup[int]:
        result: ResultLookup[int]
        if self._level == weapon_constants.StrongestWeapon:
            result = ResultLookup(errors=f"Cannot upgrade weapon past level {weapon_constants.StrongestWeapon}")
        else:
            self._level += 1
            result = ResultLookup(True, self._level)
        return result

    @property
    def level(self) -> int:
        return self._level
