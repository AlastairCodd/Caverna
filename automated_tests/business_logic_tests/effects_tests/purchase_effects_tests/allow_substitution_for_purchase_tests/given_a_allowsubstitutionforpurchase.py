from abc import ABCMeta
from typing import Dict
from unittest import TestCase

from buisness_logic.effects.purchase_effects import AllowSubstitutionForPurchaseEffect
from core.enums.caverna_enums import ResourceTypeEnum


class Given_An_AllowSubstitutionForPurchase(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self._substitute_for: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.stone: 2,
            ResourceTypeEnum.wood: 1,
        }
        self._substitute_with: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.grain: 1,
            ResourceTypeEnum.coin: 4,
        }

        self.SUT: AllowSubstitutionForPurchaseEffect = AllowSubstitutionForPurchaseEffect(
            self._substitute_for,
            self._substitute_with)
        self.because()

    def because(self) -> None:
        pass
