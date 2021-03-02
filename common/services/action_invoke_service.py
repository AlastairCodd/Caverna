from typing import List

from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from core.repositories.base_player_repository import BasePlayerRepository
from common.entities.result_lookup import ResultLookup
from common.services.exhaustive_action_ordering_service import ExhaustiveActionOrderingService
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_action_ordering_service import ActionOrderingService
from core.baseClasses.base_card import BaseCard


class ActionInvokeService(object):
    def __init__(self):
        self._action_ordering_service: ActionOrderingService = ExhaustiveActionOrderingService()

    def invoke(
            self,
            actions: ActionChoiceLookup,
            player: BasePlayerRepository,
            current_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        if actions is None:
            raise ValueError
        if player is None:
            raise ValueError
        if current_card is None:
            raise ValueError
        if current_dwarf is None:
            raise ValueError

        print(repr(actions))

        actions_best_order: ResultLookup[List[BaseAction]] = self._action_ordering_service \
            .calculated_best_order(
            actions,
            player,
            current_card,
            current_dwarf)

        success: bool = True
        successful_actions: int = 0
        errors: List[str] = []

        if actions_best_order.flag:
            print("> returned valid action ordering")
            for action in actions_best_order.value:
                print(f"  > Invoking {action}")

                invoke_result: ResultLookup[int] = action.invoke(
                    player,
                    current_card,
                    current_dwarf)

                if invoke_result.flag:
                    print(f"    > Success, {invoke_result.value} actions")
                else:
                    success = False
                    errors = ["Ordering Service returned invalid order"]
                    errors.extend(actions_best_order.errors)
                    errors.extend(invoke_result.errors)
                    break
                successful_actions += invoke_result.value
        else:
            success = False
            errors = ["Ordering Service could not find valid ordering"]
            errors.extend(actions_best_order.errors)

        result: ResultLookup[int] = ResultLookup(success, successful_actions, errors)
        return result
