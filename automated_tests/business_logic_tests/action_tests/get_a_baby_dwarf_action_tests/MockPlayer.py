from typing import Dict, List

from common.entities.player import Player
from core.baseClasses.base_effect import BaseEffect
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum


class MockPlayer(Player):
    def __init__(self, tiles: List[BaseTile] = []):
        Player.__init__(self, 0, 0)
        self._mock_tiles = tiles

    def get_player_choice(self, action):
        pass

    def get_player_choice_market_action(self, possible_items_and_costs: Dict[ResourceTypeEnum, int]) \
            -> List[ResourceTypeEnum]:
        pass

    @property
    def tiles(self) -> List[BaseTile]:
        if any(self._mock_tiles):
            return self._mock_tiles
        return super().tiles
