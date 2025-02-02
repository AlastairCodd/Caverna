from abc import ABCMeta
from typing import Union
from unittest import TestCase

from buisness_logic.services.turn_transfer_service import TurnTransferService
from common.entities.dwarf import Dwarf
from common.entities.multiconditional import Conditional
from common.entities.weapon import Weapon
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard


# noinspection PyPep8Naming


class Given_A_TurnExecutionService(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: TurnTransferService = TurnTransferService()
        self.because()

    def because(self) -> None:
        pass

    def _initialise_dwarf(
            self,
            dwarf_weapon_level: int = 0,
            is_adult: bool = True,
            is_active: bool = False,
            active_card: Union[BaseCard, None] = None):
        dwarf: Dwarf = Dwarf()
        if is_adult:
            dwarf.make_adult()

        if dwarf_weapon_level > 0:
            dwarf.give_weapon(Weapon(level=dwarf_weapon_level))

        if is_active:
            if active_card is None:
                active_card = FakeCard()
            dwarf.set_active(active_card)

        return dwarf


class FakeCard(BaseCard):
    def __init__(self,
                 name: str = "fake card",
                 card_id: int = -1,
                 actions: Union[BaseAction, Conditional, None] = None):
        super().__init__(name, card_id, actions=actions)
