from typing import List

from buisness_logic.services.base_action_player_choice_transfer_service import BaseActionPlayerChoiceTransferService
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from common.entities.precedes_constraint import PrecedesConstraint
from common.services.conditional_service import ConditionalService
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_constraint import BaseConstraint
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.enums.harvest_type_enum import HarvestTypeEnum


class CompleteActionPlayerChoiceTransferService(BaseActionPlayerChoiceTransferService):
    def __init__(self):
        self._conditionalService: ConditionalService = ConditionalService()

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

        action_choices: List[ActionChoiceLookup] = self._conditionalService.get_possible_choices(card.actions, player)

        player_action_choice_result: ResultLookup[ActionChoiceLookup] = player.get_player_choice_actions_to_use(
            action_choices,
            turn_index,
            round_index,
            harvest_type)

        success: bool = player_action_choice_result.flag
        errors: List[str] = []

        errors.extend(player_action_choice_result.errors)

        result: ResultLookup[ActionChoiceLookup]

        if success:
            untested_actions: List[BaseAction] = player_action_choice_result.value.actions

            valid_actions: List[BaseAction] = []
            constraints: List[BaseConstraint] = []

            constraints.extend(player_action_choice_result.value.constraints)

            action: BaseAction
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
                        constraints.extend(set_result.value.constraints)
                        valid_actions.append(action)

                        new_action: BaseAction
                        for new_action in set_result.value.actions:
                            untested_actions.append(new_action)
                            new_constraint: BaseConstraint = PrecedesConstraint(action, new_action)
                            constraints.append(new_constraint)
                else:
                    valid_actions.append(action)

            data: ActionChoiceLookup = ActionChoiceLookup(valid_actions, constraints)
            result = ResultLookup(success, data, errors)
        else:
            result = ResultLookup(False, errors=errors)
        return result
