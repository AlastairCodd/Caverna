from typing import List, Optional

from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from common.services.bulk_action_ordering_service import BulkActionOrderingService
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_action_ordering_service import ActionOrderingService
from core.baseClasses.base_card import BaseCard
from core.repositories.base_player_repository import BasePlayerRepository


class ActionInvokeService(object):
    def __init__(
            self,
            action_ordering_service: Optional[ActionOrderingService] = None) -> None:
        self._action_ordering_service: ActionOrderingService = action_ordering_service if action_ordering_service is not None else BulkActionOrderingService()

    def invoke(
            self,
            actions: ActionChoiceLookup,
            player: BasePlayerRepository,
            current_card: BaseCard,
            current_dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[int]:
        if actions is None:
            raise ValueError
        if player is None:
            raise ValueError
        if current_card is None:
            raise ValueError
        if current_dwarf is None:
            raise ValueError

        actions_best_order: ResultLookup[List[BaseAction]] = self._action_ordering_service \
            .calculate_best_order(
            actions,
            player,
            current_card,
            current_dwarf,
            turn_descriptor)

        if not actions_best_order.flag:
            errors = ["Ordering Service could not find valid ordering"]
            errors.extend(actions_best_order.errors)
            return ResultLookup(errors=errors)

        print("> returned valid action ordering")

        successful_actions: int = 0

        for action in actions_best_order.value:
            print(f"  > Invoking {action}")

            invoke_result: ResultLookup[int] = action.invoke(
                player,
                current_card,
                current_dwarf)

            if not invoke_result.flag:
                errors = ["Ordering Service returned invalid order"]
                errors.extend(actions_best_order.errors)
                errors.extend(invoke_result.errors)
                return ResultLookup(errors=errors)

            print(f"    > Success, {invoke_result.value} actions")
            successful_actions += invoke_result.value

        result: ResultLookup[int] = ResultLookup(True, successful_actions)
        return result
