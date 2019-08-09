from core.baseClasses.base_action import BaseAction
from core.enums.caverna_enums import ActionCombinationEnum


class Conditional(object):

    def __init__(self, combination_type: ActionCombinationEnum, condition1, condition2):
        if condition1 is None:
            raise ValueError("condition1")
        if condition2 is None:
            raise ValueError("condition2")

        self._condition1 = condition1
        self._condition2 = condition2
        self._type = combination_type

    def get_left_branch(self):
        if self._condition1 is self: raise ValueError("cannot recurse conditions")
        return self._condition1

    def get_right_branch(self):
        if self._condition2 is self: raise ValueError("cannot recurse conditions")
        return self._condition2

    def get_combination_type(self):
        return self._type
