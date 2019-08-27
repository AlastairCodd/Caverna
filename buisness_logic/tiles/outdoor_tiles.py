from buisness_logic.effects import animal_storage_effects
from core.baseClasses.base_tile import BaseTile


class FieldTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(self, "Field", 100)


class Meadow(BaseTile):
    def __init__(self):
        BaseTile.__init__(self, "Meadow", 101)


class Pasture(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Pasture", 102,
            base_points=2,
            effects=[animal_storage_effects.StoreAny(2)])


class PastureTwin(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Large Pasture", 103,
            base_points=4,
            effects=[animal_storage_effects.StoreAny(4)])