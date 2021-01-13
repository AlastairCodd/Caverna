from abc import abstractmethod, ABCMeta
from typing import Dict, Iterable, Tuple, Optional

from core.enums.caverna_enums import ResourceTypeEnum


class ResourceLayoutCheckService(metaclass=ABCMeta):
    @abstractmethod
    def check_resource_layout(
            self,
            resource_layout: Dict[int, Dict[ResourceTypeEnum, int]],
            current_resources: Dict[ResourceTypeEnum, int]) \
            -> Iterable[Tuple[
                    bool,
                    Dict[int, Optional[ResourceTypeEnum]],
                    Dict[ResourceTypeEnum, int],
                    Dict[ResourceTypeEnum, int]
                ]]:
        pass
