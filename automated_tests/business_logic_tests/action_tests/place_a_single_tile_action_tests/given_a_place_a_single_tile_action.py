from abc import ABCMeta
from typing import Optional, Dict, cast, List
from unittest import TestCase

from buisness_logic.actions.place_a_single_tile_action import PlaceASingleTileAction
from buisness_logic.tiles.dwelling import Dwelling
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import TileTypeEnum, ResourceTypeEnum


class Given_A_PlaceASingleTileAction(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: PlaceASingleTileAction
        self._specific_tile: Optional[BaseTile]

        self.because()

    def initialise_sut_as_tile_type_which_is_specific(self) -> None:
        self.SUT = PlaceASingleTileAction(TileTypeEnum.meadow)

    def initialise_sut_as_tile_type_which_is_not_specific(
            self,
            override_requisite: Optional[List[TileTypeEnum]] = None) -> None:
        self.SUT = PlaceASingleTileAction(TileTypeEnum.furnishedDwelling, override_requisite=override_requisite)

    def initialise_sut_with_specific_tile(
            self,
            override_cost: Optional[Dict[ResourceTypeEnum, int]] = None,
            specific_tile: Optional[BaseTile] = None) -> None:
        if specific_tile is None:
            self._specific_tile = Dwelling()
        else:
            self._specific_tile = specific_tile
        self.SUT = PlaceASingleTileAction(
            TileTypeEnum.furnishedCavern,
            lambda: self._specific_tile,
            override_cost)

    def because(self) -> None:
        pass

    def shouldNotBeEmpty(self, iterable) -> None:
        if isinstance(iterable, list):
            self.assertGreater(len(cast(list, iterable)), 0)
        else:
            self.assertGreater(len(list(iterable)), 0)