from abc import ABCMeta
from typing import Union, Optional, List

from common.entities.multiconditional import Conditional
from common.services.resettable import Resettable
from core.baseClasses.base_action import BaseAction
from core.exceptions.invalid_operation_error import InvalidOperationError


class BaseCard(Resettable, metaclass=ABCMeta):
    def __init__(
            self,
            name: str,
            card_id: int,
            level: int = -1,
            actions: Union[BaseAction, Conditional, None] = None,
            is_visible: Optional[bool] = None) -> None:
        self._name: str = name
        self._id: int = card_id
        self._level: int = level
        self._actions: Union[BaseAction, Conditional, None] = actions

        self._is_visible: bool = True if level < 0 else False if is_visible is None else is_visible
        self._is_active: bool = False

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def level(self) -> int:
        return self._level

    @property
    def has_been_revealled(self) -> bool:
        return self._is_visible

    @property
    def is_active(self) -> bool:
        return self._is_active

    def set_active(self) -> None:
        if self._is_active:
            raise InvalidOperationError("Cannot activate a card that is already active")
        self._is_active = True

    @property
    def is_available(self) -> bool:
        return not self._is_active and self._is_visible

    @property
    def actions(self) -> Union[BaseAction, Conditional, None]:
        return self._actions

    def reveal_card(
            self,
            cards: List['BaseCard']) -> None:
        if self._is_visible:
            raise InvalidOperationError("Cannot reveal a card that is already visible")
        self._is_visible = True

    def new_turn_reset(self) -> None:
        self._is_active = False
        self._actions.new_turn_reset()
