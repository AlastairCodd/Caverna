from core.baseClasses.base_prototype import BasePrototype, T
from core.containers.resource_container import ResourceContainer


class ResourceContainerPrototype(BasePrototype[ResourceContainer]):
    def __init__(self):
        pass

    def clone(self, source: ResourceContainer) -> ResourceContainer:
        if source is None:
            raise ValueError

        target = ResourceContainer()
        self.assign(source, target)
        return target

    def assign(self, source: ResourceContainer, target: ResourceContainer) -> None:
        if source is None:
            raise ValueError
        if target is None:
            raise ValueError

        target.give_resources(source.resources)
