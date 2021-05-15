from typing import Tuple

from core.containers.resource_container import ResourceContainer
from core.services.base_encoder_service import BaseEncoderService


class ResourceContainerEncoderService(BaseEncoderService):
    def observe(self, object_to_observe: ResourceContainer) -> Tuple[int, ...]:
        result: Tuple[int] = tuple(object_to_observe.resources.values())
        return result
