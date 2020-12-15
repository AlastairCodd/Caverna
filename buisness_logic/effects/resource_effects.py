from math import floor
from abc import abstractmethod, ABCMeta
from typing import Dict, Callable, List

from buisness_logic.effects.base_effects import BaseOnPurchaseEffect
from common.entities.result_lookup import ResultLookup
from common.services.resettable import Resettable
from core.baseClasses.base_effect import BaseEffect
from core.enums.caverna_enums import TriggerStateEnum, ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository


class BaseResourceEffect(BaseEffect, metaclass=ABCMeta):
    @abstractmethod
    def invoke(
            self,
            player: BasePlayerRepository) -> bool:
        raise NotImplementedError("base resource effect class")


class BaseOccursForSeveralTurnsEffect(BaseEffect, Resettable, metaclass=ABCMeta):
    def __init__(
            self,
            number_of_turns: int):
        if number_of_turns < 1:
            raise IndexError("Number of turns must be positive")
        self._number_of_turns: int = number_of_turns

        BaseEffect.__init__(self)

    def new_turn_reset(self) -> None:
        if self._number_of_turns > 0:
            self._number_of_turns -= 1

    def _is_still_active(self) -> bool:
        result: bool = self._number_of_turns > 0
        return result


class ReceiveOnPurchaseEffect(BaseResourceEffect, BaseOnPurchaseEffect):
    def __init__(self, output):
        self._output = output
        BaseEffect.__init__(self)

    def invoke(self, player: BasePlayerRepository) -> bool:
        if player is None:
            raise ValueError("Player may not be null")
        result: bool = player.give_resources(self._output)
        return result


class ReceiveProportionalOnPurchaseEffect(BaseResourceEffect, BaseOnPurchaseEffect):
    def __init__(
            self,
            receive: Dict[ResourceTypeEnum, int],
            proportional_to: Dict[ResourceTypeEnum, int]) -> None:
        if receive is None:
            raise ValueError("Receive cannot be null")
        if proportional_to is None:
            raise ValueError("Proportional_to cannot be null")

        self._receive: Dict[ResourceTypeEnum, int] = receive
        self._proportional_to: Dict[ResourceTypeEnum, int] = proportional_to
        BaseResourceEffect.__init__(self)

    # TODO: this needs to be run through the ActionOrderingService, and so should be returned in the get_player_choice method
    # Or does it... this is invoked _immediately_ after the tile is purchased, and with the vanilla tile set there is only ever one receive per tile
    def invoke(self, player: BasePlayerRepository) -> bool:
        if player is None:
            raise ValueError("Player may not be null")

        number_of_resources_proportional_to: List[int] = \
            [floor(player.resources.get(r, 0) / self._proportional_to[r]) for r in self._proportional_to]
        amount_to_receive_multiplier: int = min(number_of_resources_proportional_to)
        if amount_to_receive_multiplier > 0:
            resources_to_give: Dict[ResourceTypeEnum, int] = {r: amount_to_receive_multiplier * self._receive[r] for r in self._receive}
            return player.give_resources(resources_to_give)
        else:
            return True


class ReceiveConditionallyAtStartOfTurnEffect(BaseResourceEffect):
    def __init__(
            self,
            received: Dict[ResourceTypeEnum, int],
            condition: Callable[[BasePlayerRepository], int],
            trigger_state: TriggerStateEnum = TriggerStateEnum.StartOfTurn) -> None:
        """Receive some input when some condition is true.

        :param received: The resources which are received when the condition is met. This cannot be null.
        :param condition: A function which takes a player and returns the number of times they should be given
            "received". This cannot be null.
        :param trigger_state: When does this action trigger? (Optional)
        """
        if received is None:
            raise ValueError("Received")
        if condition is None:
            raise ValueError("Condition")
        self._received: Dict[ResourceTypeEnum, int] = received
        self._condition: Callable[[BasePlayerRepository], int] = condition
        BaseEffect.__init__(self, trigger_state=trigger_state)

    def invoke(
            self,
            player: BasePlayerRepository) -> bool:
        number_of_times_condition_met: int = self._condition(player)
        if number_of_times_condition_met == 0:
            return False
        resources = {resource: self._received[resource] * number_of_times_condition_met for resource in self._received}
        return player.give_resources(resources)


class ReceiveForTurnsEffect(BaseOccursForSeveralTurnsEffect):
    def __init__(
            self,
            resources: Dict[ResourceTypeEnum, int],
            number_of_turns: int) -> None:
        if resources is None:
            raise ValueError("Resources may not be null")
        self._resources: Dict[ResourceTypeEnum, int] = resources
        BaseOccursForSeveralTurnsEffect.__init__(self, number_of_turns)

    def invoke(
            self,
            player: BasePlayerRepository) -> ResultLookup[int]:
        if player is None:
            raise ValueError("Player may not be none")

        result: ResultLookup[int]
        if self._is_still_active():
            resources_given_successfully: bool = player.give_resources(self._resources)
            result = ResultLookup(resources_given_successfully, len(self._resources))
        else:
            result = ResultLookup(True, 0, f"Action has been used for {self._number_of_turns} turns, and is exhausted.")
        return result


class ReceiveWhenReceivingEffect(BaseEffect):
    def __init__(
            self,
            receive: Dict[ResourceTypeEnum, int],
            when_receiving: Dict[ResourceTypeEnum, int]) -> None:
        if receive is None:
            raise ValueError("Receive cannot be null")
        if when_receiving is None:
            raise ValueError("when_receiving cannot be null")

        self._receive: Dict[ResourceTypeEnum, int] = receive
        self._proportional_to: Dict[ResourceTypeEnum, int] = when_receiving
        BaseEffect.__init__(self)

    def invoke(
            self,
            receiving: Dict[ResourceTypeEnum, int]) -> Dict[ResourceTypeEnum, int]:
        if receiving is None:
            raise ValueError("Receviing may not be null")

        number_of_resources_proportional_to: List[int] = [floor(receiving.get(r, 0) / self._proportional_to[r]) for r in self._proportional_to]

        amount_to_receive_multiplier: int = min(number_of_resources_proportional_to)

        resources_to_give: Dict[ResourceTypeEnum, int] = {r: amount_to_receive_multiplier * self._receive[r] for r in self._receive}
        return resources_to_give
