from abc import ABC, abstractmethod
from typing import Dict
from unittest import TestCase

from automated_tests.mocks.mock_tile import MockTile
from buisness_logic.effects.purchase_effects import AllowSubstitutionForPurchase
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum


class Given_An_AllowSubstitutionForPurchase(TestCase, ABC):
    def setUp(self) -> None:
        self._subject: BaseTile = MockTile()
        self._substitute_for: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.stone: 2,
            ResourceTypeEnum.wood: 1,
        }
        self._substitute_with: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.grain: 1,
            ResourceTypeEnum.coin: 4,
        }

        self.SUT: AllowSubstitutionForPurchase = AllowSubstitutionForPurchase(
            self._subject,
            self._substitute_for,
            self._substitute_with,
            False)
        self.because()

    def because(self) -> None:
        pass