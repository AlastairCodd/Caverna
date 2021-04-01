from abc import abstractmethod, ABCMeta
from math import floor
from typing import Dict, Callable, List

from buisness_logic.effects.base_effects import BaseOnPurchaseEffect
from buisness_logic.services.base_receive_event_service import BaseReceiveEventService
from common.entities.result_lookup import ResultLookup
from common.services.resettable import Resettable
from core.baseClasses.base_effect import BaseEffect
from core.enums.caverna_enums import ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository
from localised_resources import user_interface_res
from localised_resources.localiser import format_list_with_separator, format_resource_dict


class BaseResourceEffect(
        BaseEffect,
        BaseReceiveEventService,
        metaclass=ABCMeta):
    @abstractmethod
    def invoke(
            self,
            player: BasePlayerRepository) -> bool:
        raise NotImplementedError("base resource effect class")


class BaseOccursForSeveralTurnsEffect(
        BaseEffect,
        Resettable,
        metaclass=ABCMeta):
    def __init__(
            self,
            number_of_turns: int):
        if number_of_turns < 1:
            raise IndexError("Number of turns must be positive")
        self._number_of_turns: int = number_of_turns

    def new_turn_reset(self) -> None:
        if self._number_of_turns > 0:
            self._number_of_turns -= 1

    def _is_still_active(self) -> bool:
        result: bool = self._number_of_turns > 0
        return result


class ReceiveOnPurchaseEffect(
        BaseResourceEffect,
        BaseOnPurchaseEffect):
    def __init__(
            self,
            items_to_receive: Dict[ResourceTypeEnum, int]) -> None:
        if items_to_receive is None:
            raise ValueError("Items to Receive may not be null")
        self._items_to_receive: Dict[ResourceTypeEnum, int] = items_to_receive

    def invoke(self, player: BasePlayerRepository) -> bool:
        if player is None:
            raise ValueError("Player may not be null")
        result: bool = player.give_resources(self._items_to_receive)
        return result

    def __str__(self) -> str:
        receive_readable: str = format_resource_dict(self._items_to_receive, " and ")
        result: str = f"Receive {receive_readable} immediately"
        return result


class ReceiveOnConvertFromEffect(BaseEffect):
    def __init__(
            self,
            items_to_receive: Dict[ResourceTypeEnum, int],
            when_converting_from: ResourceTypeEnum) -> None:
        if items_to_receive is None:
            raise ValueError("Items to Receive may not be null")
        self._items_to_receive: Dict[ResourceTypeEnum, int] = items_to_receive
        self._convert_from_item: ResourceTypeEnum = when_converting_from

    @property
    def items_to_receive(self) -> Dict[ResourceTypeEnum, int]:
        return self._items_to_receive

    @property
    def convert_from_item(self) -> ResourceTypeEnum:
        return self._convert_from_item

    def __str__(self) -> str:
        receive_readable: str = format_resource_dict(self._items_to_receive, " and ")
        result: str = f"Receive {receive_readable} when converting {user_interface_res.resource_plural_name[self._convert_from_item]}"
        return result


class ReceiveProportionalOnPurchaseEffect(
        BaseResourceEffect,
        BaseOnPurchaseEffect):
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

    # TODO: this needs to be run through the ActionOrderingService, and so should be returned in the get_player_choice method
    # Or does it... this is invoked _immediately_ after the tile is purchased, and with the vanilla tile set there is only ever one receive per tile
    def invoke(self, player: BasePlayerRepository) -> bool:
        if player is None:
            raise ValueError("Player may not be null")

        number_of_resources_proportional_to: List[int] = \
            [floor(player.resources.get(r, 0) / self._proportional_to[r]) for r in self._proportional_to]
        amount_to_receive_multiplier: int = min(number_of_resources_proportional_to)
        if amount_to_receive_multiplier > 0:
            resources_to_give: Dict[ResourceTypeEnum, int] = {r: amount_to_receive_multiplier * self._receive[r] for r
                                                              in self._receive}
            return self._give_player_resources(player, resources_to_give).flag
        else:
            return True

    def __str__(self) -> str:
        receive_readable: str = format_resource_dict(self._receive, " and ")
        result: str = f"Receive {receive_readable} when tile is purchased"
        return result


class ReceiveConditionallyAtStartOfTurnEffect(
        BaseResourceEffect):
    def __init__(
            self,
            received: Dict[ResourceTypeEnum, int],
            condition: Callable[[BasePlayerRepository], int],
            condition_readable: str) -> None:
        """Receive some input when some condition is true.

        :param received: The resources which are received when the condition is met. This cannot be null.
        :param condition: A function which takes a player and returns the number of times they should be given
            "received". This cannot be null.
        """
        if received is None:
            raise ValueError("Received")
        if condition is None:
            raise ValueError("Condition")
        self._received: Dict[ResourceTypeEnum, int] = received
        self._condition: Callable[[BasePlayerRepository], int] = condition
        self._condition_readable: str = condition_readable

    def invoke(
            self,
            player: BasePlayerRepository) -> bool:
        number_of_times_condition_met: int = self._condition(player)
        if number_of_times_condition_met == 0:
            return False
        resources = {resource: self._received[resource] * number_of_times_condition_met for resource in self._received}
        return player.give_resources(resources)

    def __str__(self) -> str:
        receive_readable: str = format_resource_dict(self._received, " and ")
        result: str = f"Receive {receive_readable} at start of term {self._condition_readable}"
        return result


class ReceiveForTurnsEffect(
        BaseOccursForSeveralTurnsEffect,
        BaseReceiveEventService):
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
            result = self._give_player_resources(player, self._resources)
        else:
            result = ResultLookup(True, 0, f"Action has been used for {self._number_of_turns} turns, and is exhausted.")
        return result

    def __str__(self) -> str:
        receive_readable: str = format_resource_dict(self._resources, " and ")
        result: str = f"Receive {receive_readable} at start of term for {self._number_of_turns}"
        return result


class ReceiveWhenBreedingEffect(
        BaseEffect,
        BaseReceiveEventService):
    def __init__(
            self,
            conditional: Callable[[List[ResourceTypeEnum]], Dict[ResourceTypeEnum, int]],
            condition_readable: str) -> None:
        if conditional is None:
            raise ValueError("Conditional cannot be None")
        self._conditional: Callable[[List[ResourceTypeEnum]], Dict[ResourceTypeEnum, int]] = conditional
        self._condition_readable: str = condition_readable

    def invoke(
            self,
            player: BasePlayerRepository,
            newborn_animals: List[ResourceTypeEnum]) -> ResultLookup[int]:
        if player is None:
            raise ValueError("Player cannot be none")
        if newborn_animals is None:
            raise ValueError("Newborn animals cannot be none")

        resources_to_receive: Dict[ResourceTypeEnum, int] = self._conditional(newborn_animals)
        result: ResultLookup[int]
        if any(map(lambda v: v > 0, resources_to_receive.values())):
            result = self._give_player_resources(player, resources_to_receive)
        else:
            result = ResultLookup(True, 0)

        return result

    def __str__(self) -> str:
        result: str = f"Receive {self._condition_readable}"
        return result
