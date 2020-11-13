import math
from typing import List, Callable

from buisness_logic.tiles.point_tiles import BaseConditionalPointTile
from common.entities.point_lookup import PointLookup
from core.enums.caverna_enums import ResourceTypeEnum, TileTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository


class PointCalculationService(object):

    def __init__(self):
        self._point_actions: List[Callable[[BasePlayerRepository], PointLookup]] = [
            # +1 per animal
            lambda player: self._point_per_resource(ResourceTypeEnum.cow, player),
            lambda player: self._point_per_resource(ResourceTypeEnum.sheep, player),
            lambda player: self._point_per_resource(ResourceTypeEnum.donkey, player),
            lambda player: self._point_per_resource(ResourceTypeEnum.boar, player),
            lambda player: self._point_per_resource(ResourceTypeEnum.dog, player),

            # -2 per type of farm animal that is not owned
            lambda player: self._negative_per_missing_animal(ResourceTypeEnum.cow, player),
            lambda player: self._negative_per_missing_animal(ResourceTypeEnum.sheep, player),
            lambda player: self._negative_per_missing_animal(ResourceTypeEnum.donkey, player),
            lambda player: self._negative_per_missing_animal(ResourceTypeEnum.boar, player),

            # +0.5 per grain (rounded up)
            lambda player: PointLookup(math.ceil(player.get_resources_of_type(ResourceTypeEnum.grain) / 2)),
            # +1 per resource
            lambda player: self._point_per_resource(ResourceTypeEnum.veg, player),
            lambda player: self._point_per_resource(ResourceTypeEnum.ruby, player),
            lambda player: self._point_per_resource(ResourceTypeEnum.coin, player),

            # +1 per dwarf
            lambda player: PointLookup(len(player.get_dwarves())),

            # -1 per unused space
            lambda player: PointLookup(0, player.get_number_of_tiles_of_type(TileTypeEnum.forest)),
            lambda player: PointLookup(0, player.get_number_of_tiles_of_type(TileTypeEnum.underground)),

            # base points
            lambda player: PointLookup(sum([t.get_points() for t in player.tiles])),

            # -3 per begging marker
            lambda player: PointLookup(0, 3 * player.get_resources_of_type(ResourceTypeEnum.begging_marker)),
        ]

    def calculate_points(self, player: BasePlayerRepository) -> int:
        if player is None:
            raise ValueError(str(player))

        points: List[PointLookup] = [point_action(player) for point_action in self._point_actions]
        conditional_points = self._calculate_conditional_points(player)
        total_points = sum(points, conditional_points)
        total_score = abs(total_points)
        return total_score

    def _calculate_conditional_points(self, player: BasePlayerRepository) -> List[PointLookup]:
        conditional_point_tiles: List[BaseConditionalPointTile] = player.get_tiles_of_type(BaseConditionalPointTile)
        conditional_points: List[PointLookup] = [t.get_conditional_point(player) for t in conditional_point_tiles]
        return conditional_points

    def _point_per_resource(self, resource_type: ResourceTypeEnum, player: BasePlayerRepository) -> PointLookup:
        positive_points = player.get_resources_of_type(resource_type)
        result = PointLookup(positive_points)
        return result

    def _negative_per_missing_animal(self, animal_type: ResourceTypeEnum, player: BasePlayerRepository) -> PointLookup:
        if player.get_resources_of_type(animal_type) == 0:
            return PointLookup(0, 2)
        return PointLookup(0)