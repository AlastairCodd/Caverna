class Weapon(object):
    def __init__(self, level: int = 1):
        if level < 1 or level > 8:
            raise ValueError("level at creation must be between 1 and 8")
        self._level: int = level

    def increase_level(self) -> int:
        self._level += 1
        return self._level

    @property
    def level(self) -> int:
        return self._level
