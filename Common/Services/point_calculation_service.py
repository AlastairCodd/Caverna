import math
from typing import Dict, List, Callable

from buisness_logic.tiles.point_tiles import BaseConditionalPointTile
from common.entities.player import Player
from common.entities.point_entity import PointEntity
from core.enums.caverna_enums import ResourceTypeEnum, TileTypeEnum


class PointCalculationService(object):

    def __init__(self):
        self._point_actions: List[Callable[[Player], PointEntity]] = [
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
            lambda player: PointEntity(math.ceil(player.get_resources_of_type(ResourceTypeEnum.grain) / 2)),
            # +1 per resource
            lambda player: self._point_per_resource(ResourceTypeEnum.veg, player),
            lambda player: self._point_per_resource(ResourceTypeEnum.ruby, player),
            lambda player: self._point_per_resource(ResourceTypeEnum.coin, player),

            # +1 per dwarf
            lambda player: PointEntity(len(player.get_dwarves())),

            # -1 per unused space
            lambda player: PointEntity(0, player.get_number_of_tiles_of_type(TileTypeEnum.forest)),
            lambda player: PointEntity(0, player.get_number_of_tiles_of_type(TileTypeEnum.underground)),

            # base points
            lambda player: PointEntity(sum([t.get_points() for t in player.get_tiles()])),

            # -3 per begging marker
            lambda player: PointEntity(0, 3 * player.get_resources_of_type(ResourceTypeEnum.begging_marker)),
        ]

    def calculate_points(self, player: Player) -> int:
        if player is None: raise ValueError(str(player))

        points: List[PointEntity] = [point_action(player) for point_action in self._point_actions]
        conditional_points = self._calculate_conditional_points(player)
        total_points = sum(points, conditional_points)
        total_score = abs(total_points)
        return total_score

    def _calculate_conditional_points(self, player: Player) -> List[PointEntity]:
        conditional_point_tiles: List[BaseConditionalPointTile] = player.get_tiles_of_type(BaseConditionalPointTile)
        conditional_points: List[PointEntity] = [t.get_conditional_point(player) for t in conditional_point_tiles]
        return conditional_points

    def _point_per_resource(self, resource_type: ResourceTypeEnum, player: Player) -> PointEntity:
        positive_points = player.get_resources_of_type(resource_type)
        result = PointEntity(positive_points)
        return result

    def _negative_per_missing_animal(self, animal_type: ResourceTypeEnum, player: Player) -> PointEntity:
        if player.get_resources_of_type(animal_type) == 0:
            return PointEntity(0, 2)
        return PointEntity(0)