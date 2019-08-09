from typing import Union
from core.baseClasses.base_action import BaseAction
from core.enums.caverna_enums import ActionCombinationEnum


class Combination(object):

    def __init__(
            self,
            combination_type: ActionCombinationEnum,
            combine1,
            combine2):
        if combine1 is None:
            raise ValueError("combine1")
        if combine2 is None:
            raise ValueError("combine2")

        self._combine1 = combine1
        self._combine2 = combine2
        self._type = combination_type
