from common.prototypes.dwarf_prototype import DwarfPrototype
from common.prototypes.resource_container_prototype import ResourceContainerPrototype
from common.repositories.simple_player_repository import SimplePlayerRepository
from core.repositories.base_player_repository import BasePlayerRepository
from core.baseClasses.base_prototype import BasePrototype


class PlayerPrototype(BasePrototype[BasePlayerRepository]):
    def __init__(self):
        self._dwarf_prototype: DwarfPrototype = DwarfPrototype()
        self._resource_container_prototype: ResourceContainerPrototype = ResourceContainerPrototype()

    def clone(self, source: BasePlayerRepository) -> BasePlayerRepository:
        if source is None:
            raise ValueError

        target = SimplePlayerRepository(source.id, source.turn_index)
        self.assign(source, target)
        return target

    def assign(self, source: BasePlayerRepository, target: BasePlayerRepository) -> None:
        if source is None:
            raise ValueError
        if target is None:
            raise ValueError

        target.dwarves.clear()
        for dwarf in source.dwarves:
            target.dwarves.append(self._dwarf_prototype.clone(dwarf))