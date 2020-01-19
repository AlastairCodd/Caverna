from typing import Union, Dict, List

from common.entities.multiconditional import Conditional
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.containers.resource_container import ResourceContainer
from core.enums.caverna_enums import ResourceTypeEnum


class MockCard(BaseCard, ResourceContainer):
    def __init__(
            self,
            name: str = "Mock Card",
            card_id: int = 0,
            level: int = -1,
            actions: Union[BaseAction, Conditional, None] = None,
            resources: Union[Dict[ResourceTypeEnum, int], None] = None) -> None:
        if resources is None:
            self._resources = {}
        else:
            self._resources = resources

        if actions is None:
            actions = []

        BaseCard.__init__(
            self,
            name,
            card_id,
            level,
            actions
        )
