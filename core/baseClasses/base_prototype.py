from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Iterable, List

T = TypeVar("T")


class BaseImmutablePrototype(ABC, Generic[T]):
    @abstractmethod
    def clone(self, source: T) -> T:
        pass

    def clone_range(self, source: Iterable[T]) -> List[T]:
        if source is None:
            raise ValueError("Source may not be none")
        return [self.clone(obj) for obj in source]


class BasePrototype(BaseImmutablePrototype, ABC, Generic[T]):
    @abstractmethod
    def assign(self, source: T, target: T) -> None:
        pass
