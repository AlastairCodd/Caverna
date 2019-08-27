from buisness_logic.effects import animal_storage_effects
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum


class OreMineTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Ore Mine", 201,
            base_points=3,
            effects=[animal_storage_effects.StoreSpecific({ResourceTypeEnum.donkey: 1})])


class RubyMineTile(BaseTile):
    def __init__(self):
        BaseTile.__init__(
            self, "Ruby Mine", 202,
            base_points=4,
            effects=[animal_storage_effects.StoreSpecific({ResourceTypeEnum.donkey: 1})])