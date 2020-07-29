from abc import ABCMeta
from typing import Union

from common.entities.multiconditional import Conditional
from common.services.resettable import Resettable
from core.baseClasses.base_action import BaseAction
from core.errors.invalid_operation_error import InvalidOperationError


class BaseCard(Resettable, metaclass=ABCMeta):
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

        self._isVisible: bool = True if level < 0 else False
        self._isActive: bool = False

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
            raise InvalidOperationError("Cannot reveal a card that is already visible")
        self._isVisible = True

    def new_turn_reset(self) -> None:
        self._isActive = False
