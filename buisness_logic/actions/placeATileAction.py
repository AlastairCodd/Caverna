from typing import List

from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.enums.caverna_enums import TileTypeEnum
from core.enums.harvest_type_enum import HarvestTypeEnum


class PlaceATileAction(BasePlayerChoiceAction):
    def __init__(self, tile_type: TileTypeEnum):
        self._tileLocation: int = 0
        self._tileType: TileTypeEnum = tile_type

    def set_player_choice(
            self,
            player: Player,
            dwarf: Dwarf,
            cards: List[BaseCard],
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) -> ResultLookup[ActionChoiceLookup]:
        if player is None:
            raise ValueError("player cannot be none")
        self._tileLocation = 0
        player.get_player_choice_location_to_build(self._tileType)
        return ResultLookup(True, ActionChoiceLookup([]))

    def invoke(self, player: Player, active_card: BaseCard, current_dwarf: Dwarf) -> ResultLookup[int]:
        raise NotImplementedError

    def new_turn_reset(self):
        pass
