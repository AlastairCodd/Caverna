from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generator

T = TypeVar("T")

class BaseListPermutationForge(metaclass=ABCMeta):
    @abstractmethod
    def generate_list_permutations(
            self,
            list_to_permute: list[T]) -> Generator[list[T], None, None]:
        raise NotImplementedError
