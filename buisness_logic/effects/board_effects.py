from abc import ABCMeta, abstractmethod
from typing import Dict, List
from core.baseClasses.base_effect import BaseEffect
from core.enums.caverna_enums import TileTypeEnum
from localised_resources.localiser import format_list_with_separator


class BaseBoardEffect(BaseEffect, metaclass=ABCMeta):
    @abstractmethod
    def invoke(self, source: Dict[TileTypeEnum, List[TileTypeEnum]]) -> Dict[TileTypeEnum, List[TileTypeEnum]]:
        raise NotImplementedError("base board effect class")


class ChangeRequisiteEffect(BaseBoardEffect):
    def __init__(
            self,
            tiles: List[TileTypeEnum],
            new_requisites: List[TileTypeEnum]):
        if tiles is None:
            raise ValueError("Tiles cannot be null")
        if len(tiles) == 0:
            raise ValueError("Tiles cannot be empty")
        if new_requisites is None:
            raise ValueError("New placement requisites cannot be null")
        if len(new_requisites) == 0:
            raise ValueError("New placement requisites cannot be empty")

        self._tiles: List[TileTypeEnum] = tiles
        self._new_requisites: List[TileTypeEnum] = new_requisites

    def invoke(
            self,
            source: Dict[TileTypeEnum, List[TileTypeEnum]]) -> Dict[TileTypeEnum, List[TileTypeEnum]]:
        if source is None:
            raise ValueError()

        for tile in self._tiles:
            source[tile].extend(self._new_requisites)
        return source

    def __str__(self) -> str:
        tiles_readable: str = format_list_with_separator(self._tiles, " and ")
        requisites_readable: str = format_list_with_separator(self._new_requisites, " and ")
        result: str = f"Allow {tiles_readable} to be built on {requisites_readable}"
        return result


class FurnishTunnelsEffect(ChangeRequisiteEffect):
    def __init__(self):
        ChangeRequisiteEffect.__init__(
            self,
            [TileTypeEnum.furnishedCavern, TileTypeEnum.furnishedDwelling],
            [TileTypeEnum.tunnel, TileTypeEnum.deepTunnel])


class TwinTilesOverhangEffect(ChangeRequisiteEffect):
    def __init__(self):
        twin_tiles: List[TileTypeEnum] = [
            TileTypeEnum.cavernCavernTwin,
            TileTypeEnum.cavernTunnelTwin,
            TileTypeEnum.meadowFieldTwin,
        ]
        ChangeRequisiteEffect.__init__(
            self,
            twin_tiles,
            [TileTypeEnum.unavailable])

    def __str__(self) -> str:
        result: str = f"Allow twin tiles to overhang the edge of the board"
        return result
