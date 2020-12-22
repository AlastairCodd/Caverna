from abc import ABCMeta, abstractmethod
from typing import Dict

from common.entities.tile_entity import TileEntity


class BaseTileContainerDefault(metaclass=ABCMeta):
    @abstractmethod
    def assign(
            self,
            tile_collection: Dict[int, TileEntity]) -> Dict[int, TileEntity]:
        pass
