import math
from typing import Dict
from common.entities.player import Player
from core.enums.caverna_enums import ResourceTypeEnum


def calculate_points(player: Player):
    if player is None: raise ValueError(str(player))

    positivePoints = 0
    negativePoints = 0

    resources: Dict[ResourceTypeEnum, int] = player.get_resources()

    positivePoints += resources[ResourceTypeEnum.cow] + resources[ResourceTypeEnum.sheep] \
                      + resources[ResourceTypeEnum.boar] + resources[ResourceTypeEnum.donkey]
    if resources[ResourceTypeEnum.cow] == 0: negativePoints += 2
    if resources[ResourceTypeEnum.boar] == 0: negativePoints += 2
    if resources[ResourceTypeEnum.sheep] == 0: negativePoints += 2
    if resources[ResourceTypeEnum.donkey] == 0: negativePoints += 2

    positivePoints += math.ceil(resources[ResourceTypeEnum.grain] / 2) + resources[ResourceTypeEnum.veg] \
                      + resources[ResourceTypeEnum.ruby]

    positivePoints += len(player.get_dwarves())

    player.get_tiles()
