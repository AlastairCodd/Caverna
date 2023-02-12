from typing import List, Tuple, Dict

from buisness_logic.actions.pay_action import PayAction
from buisness_logic.actions.receive_action import ReceiveAction
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.precedes_constraint import PrecedesConstraint
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_constraint import BaseConstraint
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.enums.caverna_enums import ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository
from core.services.base_player_service import BasePlayerService


class WeeklyMarketAction(BasePlayerChoiceAction):
    def __init__(self) -> None:
        self._purchasable_items: List[Tuple[ResourceTypeEnum, int]] = [
            (ResourceTypeEnum.dog, 2),
            (ResourceTypeEnum.sheep, 1),
            (ResourceTypeEnum.donkey, 1),
            (ResourceTypeEnum.boar, 2),
            (ResourceTypeEnum.cow, 3),
            (ResourceTypeEnum.wood, 1),
            (ResourceTypeEnum.stone, 1),
            (ResourceTypeEnum.ore, 1),
            (ResourceTypeEnum.grain, 1),
            (ResourceTypeEnum.veg, 2),
        ]

    def set_player_choice(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        if player is None:
            raise ValueError("Player may not be None")
        if turn_descriptor is None:
            raise ValueError("Turn descriptor may not be None")

        market_items_result: ResultLookup[List[ResourceTypeEnum]] = player.get_player_choice_market_items_to_purchase(turn_descriptor)

        result: ResultLookup[ActionChoiceLookup]

        if not market_items_result.flag:
            return ResultLookup(False, errors=market_items_result.errors)

        success: bool = True
        errors: List[str] = []

        success &= market_items_result.flag
        errors.extend(market_items_result.errors)

        actions: List[BaseAction] = []
        constraints: List[BaseConstraint] = []

        for resource in market_items_result.value:
            if resource in self._purchasable_items:
                pay_action: PayAction = PayAction({ResourceTypeEnum.coin: self._purchasable_items[resource][1]})
                receive_action: ReceiveAction = ReceiveAction({resource: 1})

                precedes_constraints: PrecedesConstraint = PrecedesConstraint(pay_action, receive_action)

                actions.append(pay_action)
                actions.append(receive_action)

                constraints.append(precedes_constraints)
            else:
                success = False
                errors.append(f"{resource.name} cannot be purchased at market")

        action_choice: ActionChoiceLookup = ActionChoiceLookup(actions, constraints)
        result = ResultLookup(success, action_choice, errors)

        return result

    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        return ResultLookup(True, 0)

    def new_turn_reset(self) -> None:
        pass
