from typing import Dict, List

from buisness_logic.actions.payAction import PayAction
from buisness_logic.services.available_card_service import AvailableCardService
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.enums.harvest_type_enum import HarvestTypeEnum
from core.services.base_player_service import BasePlayerService
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum


class UseAnotherCardAction(BasePlayerChoiceAction, PayAction):
    def __init__(
            self,
            cost: Dict[ResourceTypeEnum, int]) -> None:
        PayAction.__init__(self, cost)
        self._available_card_service: AvailableCardService = AvailableCardService()

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
