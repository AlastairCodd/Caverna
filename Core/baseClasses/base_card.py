from abc import ABC
from typing import Union, List

from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.multiconditional import Conditional
from common.entities.player import Player
from common.services.resettable import Resettable
from core.baseClasses.base_action import BaseAction
from common.entities.dwarf import Dwarf
from common.services.conditional_service import ConditionalService
from core.containers.resource_container import ResourceContainer
from core.errors.invalid_operation_error import InvalidOperationError


class BaseCard(ABC, Resettable):
    def __init__(
            self,
            name: str,
            card_id: int,
            level: int = -1,
            actions: Union[BaseAction, Conditional] = None):
        self._name: str = name
        self._id: int = card_id
        self._level: int = level
        if actions is None:
            raise ValueError("Card.__init__ actions cannot be null")
        self._actions: Union[BaseAction, Conditional] = actions

        self._isVisible = True if level < 0 else False
        self._isActive = False

    @property
    def id(self) -> int:
        return self._id

    @property
    def level(self) -> int:
        return self._level

    @property
    def is_active(self) -> bool:
        return self._isActive

    @property
    def is_available(self) -> bool:
        return not self._isActive and self._isVisible

    @property
    def actions(self) -> Union[BaseAction, Conditional]:
        return self._actions

    def reveal_card(self) -> None:
        if self._isVisible:
            raise InvalidOperationError()
        self._isVisible = True

    def new_turn_reset(self) -> None:
        self._isActive = False

    def activate_card(
            self,
            player: Player,
            dwarf: Dwarf,
            action_choice: List[BaseAction]) -> bool:
        if player is None:
            raise ValueError("player")
        if dwarf is None:
            raise ValueError("dwarf")
        if dwarf.is_active:
            raise ValueError("dwarf cannot already be active")

        if not self.is_available:
            return False

        conditional_service: ConditionalService = ConditionalService()

        possible_choices: List[ActionChoiceLookup] = conditional_service\
            .get_possible_choices(self._actions, player)

        success: bool = action_choice in possible_choices

        if success:
            for action in action_choice:
                action.invoke(player, typing.cast(ResourceContainer, self), dwarf)
            dwarf.set_active(self)
            self._isActive = True
            
        return success
