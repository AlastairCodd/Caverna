from typing import Optional

from common.prototypes.base_tile_prototype import BaseTilePrototype
from core.baseClasses.base_prototype import BasePrototype, BaseImmutablePrototype
from core.baseClasses.base_tile import BaseTile
from core.containers.tile_container import TileContainer


class TileContainerPrototype(BasePrototype[TileContainer]):
    def __init__(self):
        self._tile_prototype: BaseImmutablePrototype[BaseTile] = BaseTilePrototype()

    def clone(self, source: TileContainer) -> TileContainer:
        if source is None:
            raise ValueError
        target = TileContainer(source.height, source.width)

        self.assign(source, target)
        return target

    def assign(self, source: TileContainer, target: TileContainer) -> None:
        # TODO: Testttt
        if source is None:
            raise ValueError("Source may not be None")
        if target is None:
            raise ValueError("Target may not be None")

        if source.height != target.height:
            raise ValueError
        if source.width != target.width:
            raise ValueError

        for i in range(source.tile_count):
            source_tile: Optional[BaseTile] = source.get_tile_at_location(i)
            if source_tile is not None:
                new_tile_clone: BaseTile = self._tile_prototype.clone(source_tile)
                target.tiles[i].set_tile(new_tile_clone)
