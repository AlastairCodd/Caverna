from abc import ABCMeta
from unittest import TestCase


# noinspection PyPep8Naming
from buisness_logic.effects.resource_effects import ReceiveProportionalOnPurchaseEffect
from core.enums.caverna_enums import ResourceTypeEnum


class Given_A_ReceiveProportionalOnPurchaseEffect(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: ReceiveProportionalOnPurchaseEffect = ReceiveProportionalOnPurchaseEffect(
            {ResourceTypeEnum.wood: 1},
            {ResourceTypeEnum.stone: 2})
        self.because()

    def because(self) -> None:
        pass
