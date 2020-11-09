from abc import ABCMeta
from typing import Optional, Dict
from unittest import TestCase

from buisness_logic.actions.placeATileAction import PlaceATileAction
from buisness_logic.tiles.dwelling import Dwelling
from core.enums.caverna_enums import TileTypeEnum, ResourceTypeEnum


class Given_A_PlaceATileAction(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: PlaceATileAction
        self.because()

    def initialise_sut_as_tile_type_which_is_specific(self) -> None:
        self.SUT = PlaceATileAction(TileTypeEnum.meadow)

    def initialise_sut_with_specific_tile(
            self,
            override_cost: Optional[Dict[ResourceTypeEnum, int]] = None) -> None:
        self.SUT = PlaceATileAction(TileTypeEnum.furnishedCavern, Dwelling, override_cost)

    def initialise_sut_with_twin_tile(
            self,
            override_cost: Optional[Dict[ResourceTypeEnum, int]] = None) -> None:
        self.SUT = PlaceATileAction(TileTypeEnum.oreMineDeepTunnelTwin, override_cost=override_cost)

    def because(self) -> None:
        pass
