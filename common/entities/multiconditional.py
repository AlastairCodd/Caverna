from typing import Dict, Callable, Any, Union

from core.baseClasses.base_action import BaseAction
from core.enums.caverna_enums import ActionCombinationEnum


class Conditional(object):
    def __init__(
            self,
            combination_type: ActionCombinationEnum,
            condition1: Union[BaseAction, 'Conditional'],
            condition2: Union[BaseAction, 'Conditional']):
        if condition1 is None:
            raise ValueError("condition1")
        if condition2 is None:
            raise ValueError("condition2")

        self._condition1: Union[BaseAction, 'Conditional'] = condition1
        self._condition2: Union[BaseAction, 'Conditional'] = condition2
        self._type: ActionCombinationEnum = combination_type

    def get_left_branch(self) -> Union[BaseAction, 'Conditional']:
        if self._condition1 is self: raise ValueError("cannot recurse conditions")
        return self._condition1

    def get_right_branch(self) -> Union[BaseAction, 'Conditional']:
        if self._condition2 is self: raise ValueError("cannot recurse conditions")
        return self._condition2

    def get_combination_type(self) -> ActionCombinationEnum:
        return self._type
