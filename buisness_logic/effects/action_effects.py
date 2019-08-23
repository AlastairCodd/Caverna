from core.baseClasses.base_effect import BaseEffect
from core.enums.caverna_enums import ActionCombinationEnum


class ChangeDecisionVerb(BaseEffect):
    def __init__(self, change_from: ActionCombinationEnum, change_to: ActionCombinationEnum):
        self._change_from = change_from
        self._change_to = change_to

    def invoke(self, combination: ActionCombinationEnum) -> ActionCombinationEnum:
        if combination == self._change_from:
            return self._change_to
        return combination