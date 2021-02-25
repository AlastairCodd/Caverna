from typing import Union, Optional

from common.entities.multiconditional import Conditional
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.containers.resource_container import ResourceContainer


class SimpleCard(BaseCard):
    pass


class SimpleResourceContainerCard(BaseCard, ResourceContainer):
    def __init__(
            self,
            name: str,
            card_id: int,
            level: int = -1,
            actions: Union[BaseAction, Conditional] = None,
            is_visible: Optional[bool] = None) -> None:
        BaseCard.__init__(
            self,
            name,
            card_id,
            level,
            actions,
            is_visible)
        ResourceContainer.__init__(self)
