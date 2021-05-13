from abc import ABCMeta, abstractmethod
from typing import Tuple, TypeVar

T = TypeVar("T")


class BaseEncoderService(metaclass=ABCMeta):
    @abstractmethod
    def observe(self, object_to_observe: T) -> Tuple[int, ...]:
        pass
