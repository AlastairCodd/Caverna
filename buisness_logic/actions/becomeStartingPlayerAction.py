from core.baseClasses.base_action import BaseAction
from common.entities.player import Player
from core.containers.resource_container import ResourceContainer


class BecomeStartingPlayerAction(BaseAction):
    def __init__(self):
        self._starting_player_next_turn: Player = None

    def invoke(self, player: Player, active_card: ResourceContainer) -> bool:
        if player is None:
            raise ValueError("player")
        self._starting_player_next_turn = player
        return True

    def new_turn_reset(self):
        self._starting_player_next_turn = None
