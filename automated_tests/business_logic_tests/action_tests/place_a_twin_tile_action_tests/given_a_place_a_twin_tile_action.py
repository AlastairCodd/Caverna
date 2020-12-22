from abc import ABCMeta
from typing import Optional, Dict, cast, List
from unittest import TestCase

from buisness_logic.actions.place_a_twin_tile_action import PlaceATwinTileAction
from buisness_logic.tiles.dwelling import Dwelling
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import TileTypeEnum, ResourceTypeEnum


class Given_A_PlaceATwinTileAction(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: PlaceATwinTileAction
        self._specific_tile: Optional[BaseTile]

        self.because()

    def initialise_sut_with_twin_tile(
            self,
            override_cost: Optional[Dict[ResourceTypeEnum, int]] = None) -> None:
        self.SUT = PlaceATwinTileAction(TileTypeEnum.oreMineDeepTunnelTwin, override_cost=override_cost)

    def because(self) -> None:
        pass

    def shouldNotBeEmpty(self, iterable) -> None:
        if isinstance(iterable, list):
            self.assertGreater(len(cast(list, iterable)), 0)
        else:
            self.assertGreater(len(list(iterable)), 0)