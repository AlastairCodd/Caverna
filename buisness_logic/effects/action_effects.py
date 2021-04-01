from core.baseClasses.base_effect import BaseEffect
from core.enums.caverna_enums import ActionCombinationEnum
from localised_resources.user_interface_res import action_combination_readable


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

    def __str__(self) -> str:
        change_from_readable: str = action_combination_readable[self._change_from]
        change_to_readable: str = action_combination_readable[self._change_to]
        result: str = f"Change decision verbs from {change_from_readable} to {change_to_readable}"
        return result
