from typing import Dict

from common.entities.dwarf import Dwarf
from common.entities.player import Player
from core.baseClasses.base_action import BaseAction
from core.containers.resource_container import ResourceContainer
from core.enums.caverna_enums import ResourceTypeEnum


class UseAnotherCardAction(BaseAction):
    def __init__(self, cost: Dict[ResourceTypeEnum, int]) -> None:
        """Allows the player to use another claimed action. 

        :param cost: The cost which must be paid by the player in order to use this action. This cannot be null.
        """

    def invoke(self, player: Player, active_card: ResourceContainer, current_dwarf: Dwarf) -> bool:
        """Allows the player to use an action which has already been claimed by another player.

        :param player: The player. This cannot be null.
        :param active_card: Unused.
        :param current_dwarf: The current dwarf. This cannot be null.
        """
        if player is None:
            raise ValueError("player")
        raise NotImplementedError()

    def new_turn_reset(self):
        pass
