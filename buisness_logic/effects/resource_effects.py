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
        BaseEffect.__init__(self, True)

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
        BaseEffect.__init__(self, False)

    def invoke(self, player: BasePlayerRepository) -> bool:
        if player is None:
            raise ValueError("Player may not be null")
        result: bool = player.give_resources(self._items_to_receive)
        return result

    def __format__(self, format_spec):
       text = [("", "receive ")]

       for (resource, amount) in self._items_to_receive.items():
           text.append(("class:count", str(amount)))
           text.append(("", " "))
           text.append(("", resource.name))
           text.append(("", ", "))

       text.append(("", "immediately, on purchase"))


class ReceiveOnConvertFromEffect(BaseEffect):
    def __init__(
            self,
            items_to_receive: Dict[ResourceTypeEnum, int],
            when_converting_from: ResourceTypeEnum) -> None:
        if items_to_receive is None:
            raise ValueError("Items to Receive may not be null")
        self._items_to_receive: Dict[ResourceTypeEnum, int] = items_to_receive
        self._convert_from_item: ResourceTypeEnum = when_converting_from
        BaseEffect.__init__(self, False)

    @property
    def items_to_receive(self) -> Dict[ResourceTypeEnum, int]:
        return self._items_to_receive

    @property
    def convert_from_item(self) -> ResourceTypeEnum:
        return self._convert_from_item


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
        BaseEffect.__init__(self, False)

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

    def __format__(self, format_spec):
       text = [("", "receive ")]

       for (i, (resource, amount)) in enumerate(self._receive.items()):
           text.append(("class:count", str(amount)))
           text.append(("", " "))
           text.append(("", resource.name))
           if i != len(self._receive) - 1:
               text.append(("", ", "))

       text.append(("", " for every "))

       for (resource, amount) in self._proportional_to.items():
           text.append(("class:count", str(amount)))
           text.append(("", " "))
           text.append(("", resource.name))
           text.append(("", ", "))

       text.append(("", "immediately, on purchase"))

       if format_spec == "pp":
          return text
       if format_spec.isspace():
          return "".join(e[1] for e in text)
       raise ValueError("format parameter must be 'pp' or whitespace/empty")


class ReceiveConditionallyAtStartOfTurnEffect(
        BaseResourceEffect):
    def __init__(
            self,
            received: Dict[ResourceTypeEnum, int],
            condition: Callable[[BasePlayerRepository], int]) -> None:
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
        BaseEffect.__init__(self, False)

    def invoke(
            self,
            player: BasePlayerRepository) -> bool:
        number_of_times_condition_met: int = self._condition(player)
        if number_of_times_condition_met == 0:
            return False
        resources = {resource: self._received[resource] * number_of_times_condition_met for resource in self._received}
        return player.give_resources(resources)


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

    def __format__(self, format_spec):
        text = [
            ("", "at the beginning of the next "),
            ("class:count", str(self._number_of_turns)),
            ("", " turns, receive "),
        ]

        for (i, (resource, amount)) in enumerate(self._resources.items()):
            text.append(("class:count", str(amount)))
            text.append(("", " "))
            text.append(("", resource.name))
            if i != len(self._resources) - 1:
                text.append(("", ", "))

        if format_spec == "pp":
            return text
        if format_spec.isspace():
            return "".join(e[1] for e in text)
        raise ValueError("format parameter must be 'pp' or whitespace/empty")


class ReceiveWhenBreedingEffect(
        BaseEffect,
        BaseReceiveEventService):
    def __init__(
            self,
            conditional: Callable[[List[ResourceTypeEnum]], Dict[ResourceTypeEnum, int]],
            conditional_repr: str) -> None:
        if conditional is None:
            raise ValueError("Conditional cannot be None")
        if conditional_repr is None or conditional_repr.isspace():
            raise ValueErorr("conditional representation cannot be null or whitespace")
        self._conditional: Callable[[List[ResourceTypeEnum]], Dict[ResourceTypeEnum, int]] = conditional
        self._conditional_repr: str = conditional_repr
        BaseEffect.__init__(self, False)

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

    def __str__(self):
       # FIXME: make class abstract, and require implementations to overload
       #        for colour reasons
       return f"receive {self._conditional_repr}"
