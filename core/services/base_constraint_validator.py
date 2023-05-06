from abc import ABCMeta, abstractmethod

from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_constraint import BaseConstraint


class BaseConstraintValidator(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, constraints: list[BaseConstraint]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_index_of_first_action_which_fails_constraints(
            self,
            permutation: list[BaseAction]) -> int:
        raise NotImplementedError
