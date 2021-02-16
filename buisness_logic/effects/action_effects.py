from core.baseClasses.base_effect import BaseEffect
from core.enums.caverna_enums import ActionCombinationEnum


class ChangeDecisionVerb(BaseEffect):
    def __init__(
            self,
            change_from: ActionCombinationEnum,
            change_to: ActionCombinationEnum):
        self._change_from: ActionCombinationEnum = change_from
        self._change_to: ActionCombinationEnum = change_to

    def invoke(
            self,
            combination: ActionCombinationEnum) -> ActionCombinationEnum:
        result: ActionCombinationEnum = combination
        if combination == self._change_from:
            result = self._change_to
        return result
