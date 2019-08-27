from abc import ABC
from typing import Union, List
from common.entities.multiconditional import Conditional
from common.entities.player import Player
from core.baseClasses.base_action import BaseAction
from common.entities.dwarf import Dwarf
from common.services.conditional_service import ConditionalService


class BaseCard(ABC):
    def __init__(
            self,
            name: str,
            card_id: int,
            level: int = -1,
            actions: Union[BaseAction, Conditional] = None):
        self._name: str = name
        self._id: int = card_id
        self._level: int = level
        self._actions: Union[BaseAction, Conditional] = actions
        self._isActive = False

    @property
    def id(self) -> int:
        return self._id

    @property
    def level(self) -> int:
        return self._level

    @property
    def is_active(self):
        return self._isActive

    @property
    def is_available(self):
        return not self._isActive

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

        if self._isActive:
            return False

        conditional_service: ConditionalService = ConditionalService()

        possible_choices: List[List[BaseAction]] = conditional_service\
            .get_possible_choices(self._actions, player)

        success: bool = action_choice in possible_choices

        if success:
            for action in action_choice:
                action.invoke(player, self, dwarf)
            dwarf.set_active(self)
        return success

    def make_available(self):
        self._isActive = False
