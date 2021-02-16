from buisness_logic.effects import food_effects
from core.baseClasses.base_tile import BaseSpecificTile
from core.constants import tile_ids
from core.enums.caverna_enums import ResourceTypeEnum, TileTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository


class WorkingCaveTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Working Cave", tile_ids.WorkingCaveTileId,
            base_points=2,
            cost={ResourceTypeEnum.wood: 1,
                  ResourceTypeEnum.stone: 2},
            effects=[
                food_effects.SubstituteFoodForDwarfEffect({ResourceTypeEnum.wood: 1}),
                food_effects.SubstituteFoodForDwarfEffect({ResourceTypeEnum.stone: 1}),
                food_effects.SubstituteFoodForDwarfEffect({ResourceTypeEnum.ore: 1})])


class MiningCaveTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Mining Cave", tile_ids.MiningCaveTileId,
            base_points=2,
            cost={ResourceTypeEnum.wood: 3,
                  ResourceTypeEnum.stone: 2},
            effects=[food_effects.DiscountEffect(self._conditional)])

    def _conditional(self, player: BasePlayerRepository) -> int:
        number_of_mines_player_has: int = player.get_number_of_tiles_of_type(TileTypeEnum.mine)
        number_of_ruby_mines_player_has: int = player.get_number_of_tiles_of_type(TileTypeEnum.rubyMine)
        number_of_donkeys_player_has: int = player.get_resources_of_type(ResourceTypeEnum.donkey)

        result: int = min(number_of_donkeys_player_has, number_of_mines_player_has + number_of_ruby_mines_player_has)
        return result
