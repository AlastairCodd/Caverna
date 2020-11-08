from abc import ABCMeta
from unittest import TestCase

from common.services.tile_service import TileService


# noinspection PyPep8Naming
class Given_A_TileService(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: TileService = TileService()
        self.because()

    def because(self) -> None:
        pass
