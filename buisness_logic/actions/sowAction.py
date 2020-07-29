from typing import Dict, List

from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.enums.harvest_type_enum import HarvestTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository
from core.services.base_player_service import BasePlayerService
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum


class SowAction(BasePlayerChoiceAction):
    def __init__(self, quantity: int = 3) -> None:
        """Sow action which allows a number of food resources to be planted, and their amount increased.

        :param quantity: Upper bound on number of seeds which can be planted. Must be positive.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        self._quantity: int = quantity
        self._grow_amount: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.grain: 2,
            ResourceTypeEnum.veg: 1
        }

    def set_player_choice(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            cards: List[BaseCard],
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) -> ResultLookup[ActionChoiceLookup]:
        # TODO: Implement this
        raise NotImplementedError()

    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        """Sows quantity seeds of some resource type, increasing the yield by the amount determined by "_grow_amount".

        :param player: The player who is planting the seeds. This cannot be null.
        :param active_card: Unused.
        :param current_dwarf: Unused.
        :return: A result lookup indicating the success of the action, and the number of seeds which were planted.
            This will never be null.
        """
        # TODO: Implement this.
        raise NotImplementedError()

    def new_turn_reset(self):
        pass
