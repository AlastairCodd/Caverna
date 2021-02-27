from typing import List

from buisness_logic.services.base_action_player_choice_transfer_service import BaseActionPlayerChoiceTransferService
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.precedes_constraint import PrecedesConstraint
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from common.services.conditional_service import ConditionalService
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_constraint import BaseConstraint
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.services.base_player_service import BasePlayerService


class CompleteActionPlayerChoiceTransferService(BaseActionPlayerChoiceTransferService):
    def __init__(self):
        self._conditional_service: ConditionalService = ConditionalService()

    def get_action(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            card: BaseCard,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        if player is None:
            raise ValueError("Player may not be None")
        if dwarf is None:
            raise ValueError("Dwarf may not be None")
        if card is None:
            raise ValueError("Card may not be None")
        if turn_descriptor is None:
            raise ValueError("Turn descriptor may not be None")

        action_choices: List[ActionChoiceLookup] = self._conditional_service.get_possible_choices(card.actions, player)

        player_action_choice_result: ResultLookup[ActionChoiceLookup]
        if len(action_choices) == 1:
            player_action_choice_result = ResultLookup(True, action_choices[0])
        else:
            player_action_choice_result = player.get_player_choice_actions_to_use(
                action_choices,
                turn_descriptor)

        return player_action_choice_result
