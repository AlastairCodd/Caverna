from typing import List, Callable, Iterable, TypeVar

from automated_tests.common_tests.service_tests.tile_service_tests.given_a_tile_service import Given_A_TileService
from buisness_logic.tiles.conversion_tiles import HuntingParlorTile
from buisness_logic.tiles.dwelling import Dwelling, SimpleStoneDwelling
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import TileTypeEnum

T = TypeVar("T")


class test_when_called_with_furnished_cavern(Given_A_TileService):
    def because(self) -> None:
        tiles: List[BaseTile] = [
            Dwelling(),
            Dwelling(),
            Dwelling(),
            SimpleStoneDwelling(),
            HuntingParlorTile()
        ]

        self._possible_tiles: List[BaseTile] = self.SUT.get_possible_tiles(
            tiles,
            TileTypeEnum.furnishedCavern)

        self._expected_tiles: List[BaseTile] = []
        self._expected_tiles.append(tiles[0])
        self._expected_tiles.extend(tiles[3:])

    def test_then_result_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._possible_tiles)

    def test_then_result_should_not_be_empty(self) -> None:
        self.assertGreater(len(self._possible_tiles), 0)

    def test_then_result_length_should_be_expected(self) -> None:
        self.assertEqual(len(self._possible_tiles), len(self._expected_tiles))

    def test_then_result_should_contain_expected_tiles(self) -> None:
        for tile in self._expected_tiles:
            with self.subTest(tile=tile):
                self.assertContains(lambda x: x.id == tile.id, self._possible_tiles)

    def assertContains(
            self,
            predicate: Callable[[T], bool],
            collection: Iterable[T]) -> None:
        if predicate is None:
            raise ValueError
        if collection is None:
            raise ValueError

        for item in collection:
            if predicate(item):
                return

        raise AssertionError("Collection should contain element satisfying predicate, but does not.")
