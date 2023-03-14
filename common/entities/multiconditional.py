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
        self._logging = True

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
        # this is a mess. even if the consumer doesn't want it as tuple pairs, we
        #    still enforce that it is, and then turn it back. which is what we do
        #    for each of the individual methods too, but not to this weird extent

        left_formatted = self._ensure_colour_printable(self._condition1.__format__(format_spec))
        right_formatted = self._ensure_colour_printable(self._condition2.__format__(format_spec))

        newline_separator = " "
        try:
            num_spaces_on_newline = int(format_spec.strip("pp"))
            if num_spaces_on_newline != 0:
                newline_separator = "\r\n" + " " * num_spaces_on_newline
        except ValueError:
            pass

        result = self._get_colour_printable(left_formatted, right_formatted, newline_separator)
        if "pp" in format_spec:
            return result
        return "".join(e[1] for e in result)

    def _ensure_colour_printable(self, formatted):
        if isinstance(formatted, list):
            return formatted
        if self._logging:
            print(f"[WRN] forcing colour printable result: action={formatted}")
        return [("", formatted)]

    def _get_colour_printable(self, left_formatted, right_formatted, newline_separator):
        if self._type is ActionCombinationEnum.EitherOr:
            text = [("", "Either ")]
            text.extend(left_formatted)
            text.append(("", " or"))
            text.append(("", newline_separator))
            text.extend(right_formatted)
            return text
        if self._type is ActionCombinationEnum.AndOr:
            text = []
            text.extend(left_formatted)
            text.append(("", " and "))
            text.extend(right_formatted)
            text.append(("", " or"))
            text.append(("", newline_separator))
            text.extend(left_formatted)
            text.append(("", " or"))
            text.append(("", newline_separator))
            text.extend(right_formatted)
            return text
        if self._type is ActionCombinationEnum.And:
            text = []
            text.extend(left_formatted)
            text.append(("", " and "))
            text.extend(right_formatted)
            return text
        if self._type is ActionCombinationEnum.AndThenOr:
            text = []
            text.extend(left_formatted)
            text.append(("", " and then "))
            text.extend(right_formatted)
            text.append(("", " or"))
            text.append(("", newline_separator))
            text.extend(left_formatted)
            text.append(("", " or"))
            text.append(("", newline_separator))
            text.extend(right_formatted)
            return text
        if self._type is ActionCombinationEnum.OrAndThenStrict:
            text = []
            text.extend(left_formatted)
            text.append(("", " and then "))
            text.extend(right_formatted)
            text.append(("", " or"))
            text.append(("", newline_separator))
            text.extend(left_formatted)
            return text
        if self._type is ActionCombinationEnum.Or:
            text = []
            text.extend(left_formatted)
            text.append(("", " or"))
            text.append(("", newline_separator))
            text.extend(right_formatted)
            return text
        if self._type is ActionCombinationEnum.AndThen:
            text = []
            text.extend(left_formatted)
            text.append(("", " and then "))
            text.extend(right_formatted)
            return text
