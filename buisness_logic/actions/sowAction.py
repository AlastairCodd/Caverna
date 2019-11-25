from typing import Dict

from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_action import BaseAction
from core.enums.caverna_enums import ResourceTypeEnum


class SowAction(BaseAction):
    def __init__(self, quantity: int = 3) -> None:
        """Sow action which allows seeds (defined in qrow_amount) to be planted, and duplicated.

        :param quantity: Upper bound on number of seeds which can be planted. Must be positive.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        self._quantity: int = quantity
        self._grow_amount: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.grain: 2,
            ResourceTypeEnum.veg: 1
        }

    def invoke(self, player: Player, active_card: BaseCard, current_dwarf: Dwarf) -> ResultLookup[int]:
        """Sows quantity seeds of some resource type, increasing the yield by the amount determined by "_grow_amount".

        :param player: The player. This cannot be null.
        :param active_card: Unused.
        :param current_dwarf: Unused.
        :returns: True if the seeds were successfully planted, false if not.
        """
        raise NotImplementedError()

    def new_turn_reset(self):
        pass
