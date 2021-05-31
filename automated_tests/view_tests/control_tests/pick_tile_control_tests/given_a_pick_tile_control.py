from abc import ABCMeta
from unittest import TestCase

from view.ui_controls.pick_tile_control import PickTileControl


# noinspection PyPep8Naming
class Given_A_PickTileControl(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: PickTileControl = PickTileControl(None)
        self.because()

    def because(self) -> None:
        pass
