from core.enums.caverna_enums import ActionCombinationEnum

class Conditional(object):
    
    def __init__(self, type: ActionCombinationEnum, condition1, condition2):
        if condition1 is None:
            raise ValueError("condition1")
        if condition2 is None:
            raise ValueError("condition2")
            
        self._condition1 = condition1
        self._condition2 = condition2
        self._type = type