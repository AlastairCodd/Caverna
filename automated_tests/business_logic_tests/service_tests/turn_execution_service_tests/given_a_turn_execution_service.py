from abc import ABC
from unittest import TestCase, mock

# noinspection PyPep8Naming
from buisness_logic.services.turn_execution_service import TurnExecutionService
from common.entities.dwarf import Dwarf
from common.entities.weapon import Weapon


class Given_A_TurnExecutionService(TestCase, ABC):
    def setUp(self) -> None:
        self.SUT: TurnExecutionService = TurnExecutionService()
        self.because()

    def because(self) -> None:
        pass

    def _initialise_dwarf(
            self,
            dwarf_weapon_level: int = 0,
            is_adult: bool = True):
        dwarf: Dwarf = mock.MagicMock(spec=Dwarf)
        dwarf.is_adult.return_value = is_adult

        if dwarf_weapon_level < 1:
            dwarf.has_weapon.return_value = False
            dwarf.weapon.return_value = None
            dwarf.weapon_level.return_value = 0
        else:
            dwarf.has_weapon.return_value = True

            dwarf_weapon: Weapon = mock.Mock(spec=Weapon)
            dwarf.weapon.return_value = dwarf_weapon
            dwarf_weapon.level.return_value = dwarf_weapon_level
            dwarf.weapon_level.return_value = dwarf_weapon_level

        return dwarf