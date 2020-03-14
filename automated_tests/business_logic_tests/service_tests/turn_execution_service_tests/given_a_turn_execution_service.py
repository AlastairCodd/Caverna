from abc import ABC
from unittest import TestCase, mock

# noinspection PyPep8Naming
from unittest.mock import patch, PropertyMock

from buisness_logic.services.turn_execution_service import TurnExecutionService
from common.entities.dwarf import Dwarf
from common.entities.weapon import Weapon
from core.baseClasses.base_card import BaseCard


class Given_A_TurnExecutionService(TestCase, ABC):
    def setUp(self) -> None:
        self.SUT: TurnExecutionService = TurnExecutionService()
        self.because()

    def because(self) -> None:
        pass

    def _initialise_dwarf(
            self,
            dwarf_weapon_level: int = 0,
            is_adult: bool = True,
            is_active: bool = False):
        dwarf: Dwarf = Dwarf()
        if is_adult:
            dwarf.make_adult()

        if dwarf_weapon_level > 0:
            dwarf.give_weapon(Weapon(level=dwarf_weapon_level))

        if is_active:
            card: BaseCard = FakeCard()
            dwarf.set_active(card)

        return dwarf


class FakeCard(BaseCard):
    def __init__(self, name: str = "fake card", card_id: int = -1):
        super().__init__(name, card_id)
