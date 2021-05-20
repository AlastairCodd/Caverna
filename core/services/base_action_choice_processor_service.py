from abc import ABCMeta
from typing import List


class BaseActionChoiceProcessorService(metaclass=ABCMeta):
    def __init__(
            self,
            length: int) -> None:
        if length < 0:
            raise ValueError("Action Choice Length must be positive")
        self._length: int = length
        self.offset: int = 0
        self._invalid_actions: List[int] = []

        self._action_choice: List[float] = []

    @property
    def length(self) -> int:
        return self._length

    def set_action_choice(
            self,
            action_choice: List[float]) -> None:
        self._action_choice = action_choice
        self._invalid_actions.clear()

    def mark_invalid_action(
            self,
            index: int) -> None:
        if index < 0 or index >= self._length:
            raise ValueError(f"Index must be between zero and {self._length}")
        if index in self._invalid_actions:
            raise ValueError("Index is already marked as invalid")
        self._invalid_actions.append(index)
