from typing import Union

from common.entities.multiconditional import Conditional
from common.entities.simple_card import SimpleResourceContainerCard, SimpleCard
from common.prototypes.resource_container_prototype import ResourceContainerPrototype
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_prototype import BaseImmutablePrototype, BasePrototype
from core.containers.resource_container import ResourceContainer


class CardPrototype(BaseImmutablePrototype[BaseCard]):
    def __init__(self) -> None:
        self._resource_container_prototype: BasePrototype[ResourceContainer] = ResourceContainerPrototype()

    def clone(self, source: BaseCard) -> BaseCard:
        if source is None:
            raise ValueError("Source may not be None")

        source_name: str = source.name
        source_id: int = source.id
        source_level: int = source.level
        source_is_visible: bool = source.is_active or source.is_available

        source_actions: Union[BaseAction, Conditional] = source.actions

        result: BaseCard
        if isinstance(source, ResourceContainer):
            result = SimpleResourceContainerCard(
                source_name,
                source_id,
                source_level,
                source_actions,
                source_is_visible
            )

            # noinspection PyTypeChecker
            self._resource_container_prototype.assign(source, result)
        else:
            result = SimpleCard(
                source_name,
                source_id,
                source_level,
                source_actions,
                source_is_visible
            )

        return result
