from abc import ABCMeta
from typing import Optional, Dict, cast
from unittest import TestCase

from buisness_logic.actions.placeATileAction import PlaceATileAction
from buisness_logic.tiles.dwelling import Dwelling
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import TileTypeEnum, ResourceTypeEnum


class Given_A_PlaceATileAction(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: PlaceATileAction
        self._specific_tile: Optional[BaseTile]

        self.because()

    def initialise_sut_as_tile_type_which_is_specific(self) -> None:
        self.SUT = PlaceATileAction(TileTypeEnum.meadow)

    def initialise_sut_with_specific_tile(
            self,
            override_cost: Optional[Dict[ResourceTypeEnum, int]] = None) -> None:
        self._specific_tile = Dwelling()
        self.SUT = PlaceATileAction(
            TileTypeEnum.furnishedCavern,
            lambda: self._specific_tile,
            override_cost)

    def initialise_sut_with_twin_tile(
            self,
            override_cost: Optional[Dict[ResourceTypeEnum, int]] = None) -> None:
        self.SUT = PlaceATileAction(TileTypeEnum.oreMineDeepTunnelTwin, override_cost=override_cost)

    def because(self) -> None:
        pass

    def shouldNotBeEmpty(self, iterable) -> None:
        if isinstance(iterable, list):
            self.assertGreater(len(cast(list, iterable)), 0)
        else:
            self.assertGreater(len(list(iterable)), 0)