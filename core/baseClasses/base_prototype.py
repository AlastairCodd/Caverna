from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")


class BaseImmutablePrototype(ABC, Generic[T]):
    @abstractmethod
    def clone(self, source: T) -> T:
        pass


class BasePrototype(BaseImmutablePrototype, ABC, Generic[T]):
    @abstractmethod
    def assign(self, source: T, target: T) -> None:
        pass
