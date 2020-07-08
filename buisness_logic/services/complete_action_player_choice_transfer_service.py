from typing import List

from buisness_logic.services.base_action_player_choice_transfer_service import BaseActionPlayerChoiceTransferService
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from common.services.conditional_service import ConditionalService
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_constraint import BaseConstraint
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.enums.harvest_type_enum import HarvestTypeEnum


class CompleteActionPlayerChoiceTransferService(BaseActionPlayerChoiceTransferService):
    def __init__(self):
        self._conditionalService: ConditionalService = ConditionalService()
        self._actionChoiceLookupBuilder = None

    def get_action(
            self,
            player: Player,
            dwarf: Dwarf,
            card: BaseCard,
            cards: List[BaseCard],
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) -> ResultLookup[ActionChoiceLookup]:
        if player is None:
            raise ValueError("Player may not be None")
        if dwarf is None:
            raise ValueError("Dwarf may not be None")
        if card is None:
            raise ValueError("Card may not be None")

        untested_actions: List[ActionChoiceLookup] = self._conditionalService.get_possible_choices(card.actions, player)

        success: bool = True
        errors: List[str] = []

        valid_actions: List[BaseAction] = []
        constraints: List[BaseConstraint] = []

        for action in untested_actions:
            if isinstance(action, BasePlayerChoiceAction):
                set_result: ResultLookup[ActionChoiceLookup] = action.set_player_choice(
                    player,
                    dwarf,
                    cards,
                    turn_index,
                    round_index,
                    harvest_type)

                success &= set_result.flag
                errors.extend(set_result.errors)

                if set_result.flag:
                    untested_actions.extend(set_result.value.actions)

        data: ActionChoiceLookup = ActionChoiceLookup(valid_actions, constraints)
        result: ResultLookup[ActionChoiceLookup] = ResultLookup(success, data, errors)
        return result
