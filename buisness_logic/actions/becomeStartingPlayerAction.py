from typing import Dict
from core.enums.caverna_enums import ResourceTypeEnum
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_action import BaseAction
from common.entities.player import Player


class BecomeStartingPlayerAction(BaseAction):
    def __init__(self):
        self._starting_player_next_turn: Player = None

    def invoke(
            self,
            player: Player,
            activeCard: BaseCard) -> bool:
        if player is None:
            raise ValueError("player")
        if activeCard is None:
            raise ValueError(str(activeCard))

        if activeCard.is_active:
            return False

        self._starting_player_next_turn = player
        return True
