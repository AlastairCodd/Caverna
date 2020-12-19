from typing import Dict

from buisness_logic.actions.pay_action import PayAction
from buisness_logic.services.available_card_service import AvailableCardService
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.enums.caverna_enums import ResourceTypeEnum
from core.services.base_player_service import BasePlayerService


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
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        # TODO: Implement this
        raise NotImplementedError()
