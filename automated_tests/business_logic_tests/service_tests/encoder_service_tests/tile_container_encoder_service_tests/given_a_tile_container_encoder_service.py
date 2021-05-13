from abc import ABCMeta
from unittest import TestCase

from buisness_logic.services.encoder_services.tile_container_encoder_service import TileContainerEncoderService


# noinspection PyPep8Naming
class Given_A_TileContainerEncoderService(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: TileContainerEncoderService = TileContainerEncoderService()
        self.because()

    def because(self) -> None:
        pass
