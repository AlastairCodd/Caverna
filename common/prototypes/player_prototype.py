from common.prototypes.dwarf_prototype import DwarfPrototype
from common.prototypes.resource_container_prototype import ResourceContainerPrototype
from common.prototypes.tile_container_prototype import TileContainerPrototype
from common.repositories.simple_player_repository import SimplePlayerRepository
from core.containers.resource_container import ResourceContainer
from core.containers.tile_container import TileContainer
from core.repositories.base_player_repository import BasePlayerRepository
from core.baseClasses.base_prototype import BasePrototype


class PlayerPrototype(BasePrototype[BasePlayerRepository]):
    def __init__(self):
        self._dwarf_prototype: DwarfPrototype = DwarfPrototype()
        self._resource_container_prototype: BasePrototype[ResourceContainer] = ResourceContainerPrototype()
        self._tile_container_prototype: BasePrototype[TileContainer] = TileContainerPrototype()

    def clone(self, source: BasePlayerRepository) -> BasePlayerRepository:
        if source is None:
            raise ValueError

        target = SimplePlayerRepository(source.id, source.descriptor, source.turn_index)
        self.assign(source, target)
        return target

    def assign(self, source: BasePlayerRepository, target: BasePlayerRepository) -> None:
        if source is None:
            raise ValueError
        if target is None:
            raise ValueError

        self._resource_container_prototype.assign(source, target)
        self._tile_container_prototype.assign(source, target)

        target.dwarves.clear()
        for dwarf in source.dwarves:
            target.dwarves.append(self._dwarf_prototype.clone(dwarf))