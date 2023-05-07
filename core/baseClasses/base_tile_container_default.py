from abc import ABCMeta, abstractmethod
from typing import Dict, Callable

from common.entities.tile_entity import TileEntity
from core.baseClasses.base_tile import BaseTile


class BaseTileContainerDefault(metaclass=ABCMeta):
    @abstractmethod
    def assign(
            self,
            tile_collection: Dict[int, TileEntity]) -> Dict[int, TileEntity]:
        pass

    @abstractmethod
    def set_on_tile_changed_callback(
            self,
            callback: Callable[[int, BaseTile], None]) -> None:
        raise NotImplementedError()
