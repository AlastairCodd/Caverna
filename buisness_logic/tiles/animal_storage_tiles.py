from typing import List

from buisness_logic.effects.allow_farming_effect import AllowFarmingEffect
from common.entities.tile_entity import TileEntity
from core.baseClasses.base_tile import BaseSpecificTile
from core.constants import tile_ids, resource_types
from core.enums.caverna_enums import ResourceTypeEnum
from buisness_logic.effects import *
from core.repositories.base_player_repository import BasePlayerRepository


class CuddleRoomTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Cuddle Room", tile_ids.CuddleRoomTileId,
            base_points=2,
            cost={ResourceTypeEnum.wood: 1},
            effects=[animal_storage_effects.StoreConditionalAnimalEffect(ResourceTypeEnum.sheep, lambda p: len(p.dwarves))])


class BreakfastRoomTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Breakfast Room", tile_ids.BreakfastRoomTileId,
            cost={ResourceTypeEnum.wood: 1},
            effects=[animal_storage_effects.StoreSpecificAnimalEffect({ResourceTypeEnum.cow: 3})])


class StubbleRoomTile(BaseSpecificTile):
    def __init__(self):
        BaseSpecificTile.__init__(
            self, "Stubble Room", tile_ids.StubbleRoomTileId,
            base_points=1,
            cost={ResourceTypeEnum.wood: 1, ResourceTypeEnum.ore: 1},
            effects=[animal_storage_effects.ChangeAnimalStorageBaseEffect(
                [ResourceTypeEnum.field],
                {animal_type: 1 for animal_type in resource_types.farm_animals},
                self._condition)])

    def _condition(
            self,
            unused_player: BasePlayerRepository,
            tile: TileEntity) -> int:
        if tile is None:
            raise ValueError("Tile cannot be none")
        allow_farming_effects: List[AllowFarmingEffect] = tile.get_effects_of_type(AllowFarmingEffect)

        result: int = 0

        if len(allow_farming_effects) > 0:
            is_anything_planted_on_this_tile: bool = False
            for effect in allow_farming_effects:
                if effect.planted_resource_type is not None:
                    is_anything_planted_on_this_tile = True
                    break

            if not is_anything_planted_on_this_tile:
                result = 1

        return result

