from typing import Tuple, List

from buisness_logic.effects.allow_farming_effect import AllowFarmingEffect
from core.constants import tile_ids
from core.containers.tile_container import TileContainer
from core.enums.caverna_enums import TileTypeEnum, ResourceTypeEnum
from core.services.base_observation_service import BaseObservationService


class TileContainerEncoderService(BaseObservationService):
    def observe(self, object_to_observe: TileContainer) -> Tuple[int, ...]:
        result: List[int] = []
        for location, tile_entity in object_to_observe.tiles.items():
            type_section: List[int] = [0 for _ in range(max(tile_type.value for tile_type in TileTypeEnum) - 1)]
            type_section[tile_entity.tile_type.value - 1] = True

            specific_tile_section: List[int] = [0 for _ in range(tile_ids.total_number_of_tiles)]
            resources_section: List[int] = [0, 0]

            if tile_entity.tile is not None:
                if tile_entity.tile.id < tile_ids.total_number_of_tiles:
                    specific_tile_section[tile_entity.tile.id] = True
                storage_effects: List[AllowFarmingEffect] = tile_entity.get_effects_of_type(AllowFarmingEffect)
                for effect in storage_effects:
                    if effect.planted_resource_type == ResourceTypeEnum.grain:
                        resources_section[0] += effect.planted_resource_amount
                    elif effect.planted_resource_type == ResourceTypeEnum.veg:
                        resources_section[1] += effect.planted_resource_amount

            tile_section: List[int] = type_section
            tile_section.extend(specific_tile_section)
            tile_section.extend(resources_section)

            result.extend(tile_section)

        return (* result, )
