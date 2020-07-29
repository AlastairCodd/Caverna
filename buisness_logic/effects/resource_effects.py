from abc import abstractmethod, ABCMeta
from typing import Dict, Callable

from core.baseClasses.base_effect import BaseEffect
from core.enums.caverna_enums import TriggerStateEnum, ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository


class BaseResourceEffect(BaseEffect, metaclass=ABCMeta):
    @abstractmethod
    def invoke(
            self,
            player: BasePlayerRepository) -> bool:
        raise NotImplementedError("base resource effect class")


class Receive(BaseResourceEffect):
    def __init__(self, output):
        self._output = output
        BaseEffect.__init__(self)

    def invoke(self, player: BasePlayerRepository) -> bool:
        # TODO: Implement
        raise NotImplementedError()


class ReceiveConditional(BaseResourceEffect):
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
