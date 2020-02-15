from abc import ABC, abstractmethod
from unittest import TestCase

from common.services.camel_service import CamelService


class Given_A_CamelService(ABC, TestCase):
    def setUp(self) -> None:
        self.SUT: CamelService = CamelService()
        self.because()

    @abstractmethod
    def because(self):
        pass