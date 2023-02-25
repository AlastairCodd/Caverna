from typing import Dict, Callable, Any, Union

from core.baseClasses.base_action import BaseAction
from core.enums.caverna_enums import ActionCombinationEnum
from common.services.resettable import Resettable


class Conditional(Resettable):
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
        if self._condition1 is self:
            raise ValueError("cannot recurse conditions")
        return self._condition1

    def get_right_branch(self) -> Union[BaseAction, 'Conditional']:
        if self._condition2 is self:
            raise ValueError("cannot recurse conditions")
        return self._condition2

    def get_combination_type(self) -> ActionCombinationEnum:
        return self._type

    def new_turn_reset(self) -> None:
        self._condition1.new_turn_reset()
        self._condition2.new_turn_reset()

    def __str__(self) -> str:
        return self.__format__("")

    def __format__(self, format_spec) -> str:
        type_to_string: Dict[ActionCombinationEnum, Callable[[Any, Any], str]] = {
            ActionCombinationEnum.EitherOr: lambda c1, c2: f"Either {self._condition1:{format_spec}} or {self._condition2:{format_spec}}",
            ActionCombinationEnum.AndOr: lambda c1, c2: f"{self._condition1:{format_spec}} and/or {self._condition2:{format_spec}}",
            ActionCombinationEnum.And: lambda c1, c2: f"{self._condition1:{format_spec}} and {self._condition2:{format_spec}}",
            ActionCombinationEnum.AndOptionally: lambda c1, c2: f"{self._condition1:{format_spec}} and/or {self._condition2:{format_spec}}",
            ActionCombinationEnum.AndThenOr: lambda c1, c2: f"{self._condition1:{format_spec}} and then/or {self._condition2:{format_spec}}",
            ActionCombinationEnum.OrAndThen: lambda c1, c2: f"{self._condition1:{format_spec}} and then {self._condition2:{format_spec}}, or {self._condition1:{format_spec}}",
            ActionCombinationEnum.Or: lambda c1, c2: f"{self._condition1:{format_spec}} or {self._condition2:{format_spec}}",
            ActionCombinationEnum.AndThen: lambda c1, c2: f"{self._condition1:{format_spec}} and then {self._condition2:{format_spec}}",
        }
        result: str = type_to_string[self._type](self._condition1, self._condition2)
        return result
