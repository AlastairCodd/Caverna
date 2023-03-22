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
        self._purchasable_items: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.dog: 2,
            ResourceTypeEnum.sheep: 1,
            ResourceTypeEnum.donkey: 1,
            ResourceTypeEnum.boar: 2,
            ResourceTypeEnum.cow: 3,
            ResourceTypeEnum.wood: 1,
            ResourceTypeEnum.stone: 1,
            ResourceTypeEnum.ore: 1,
            ResourceTypeEnum.grain: 1,
            ResourceTypeEnum.veg: 2,
        }

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
            if resource not in self._purchasable_items:
                success = False
                errors.append(f"{resource.name} cannot be purchased at market")
                continue
            pay_action: PayAction = PayAction({ResourceTypeEnum.coin: self._purchasable_items[resource]})
            receive_action: ReceiveAction = ReceiveAction({resource: 1})

            precedes_constraints: PrecedesConstraint = PrecedesConstraint(pay_action, receive_action)

            actions.append(pay_action)
            actions.append(receive_action)

            constraints.append(precedes_constraints)

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

    def __str__(self) -> str:
        return self.__format__("")

    def __format__(self, format_spec) -> str:
        newline_separator = ""
        long_separator = separator = " "

        try:
            num_spaces = int(format_spec.strip("p"))
            if num_spaces != 0 and not format_spec.isspace():
                newline_separator = "\r\n"
                separator = " " * num_spaces
                long_separator = " " * num_spaces * 2
        except ValueError:
            pass

        text = [
            ("", "buy from"),
            ("", f"{newline_separator}{long_separator}")
        ]

        for (i, (resource, cost)) in enumerate(self._purchasable_items.items()):
            text.append(("class:resource:", resource.name))
            text.append(("", " ("))
            text.append(("class:count", str(cost)))
            text.append(("", " "))
            if cost > 1:
                text.append(("class:resource", "coins"))
            else:
                text.append(("class:resource", "coin"))
            text.append(("", ")"))
            if i != len(self._purchasable_items) - 1:
                text.append(("", ","))
                text.append(("", f"{newline_separator}{long_separator}"))

        text.append(("", f"{newline_separator}{separator}"))
        text.append(("", "(maximum of "))
        text.append(("class:count", "one"))
        text.append(("", " purchase per resource)"))

        if "pp" in format_spec:
            return text
        return "".join(e[1] for e in text)

    def __repr__(self) -> str:
        return "WeeklyMarketAction()"
