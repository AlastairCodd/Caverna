from core.baseClasses.base_effect import BaseEffect
from core.enums.caverna_enums import ActionCombinationEnum


class ChangeDecisionVerb(BaseEffect):
    def __init__(
            self,
            change_from: ActionCombinationEnum,
            change_to: ActionCombinationEnum):
        self._change_from: ActionCombinationEnum = change_from
        self._change_to: ActionCombinationEnum = change_to
        BaseEffect.__init__(self, False)

    def invoke(
            self,
            combination: ActionCombinationEnum) -> ActionCombinationEnum:
        result: ActionCombinationEnum = combination
        if combination == self._change_from:
            result = self._change_to
        return result

    def __format__(self, format_spec):
        text = [
            ("", self._change_from.name),
            ("", " becomes "),
            ("", self._change_to.name),
            ("", " for you"),
        ]

        if format_spec == "pp":
            return text
        if format_spec.isspace():
            return "".join(e[1] for e in text)
        raise ValueError("format parameter must be 'pp' or whitespace/empty")
