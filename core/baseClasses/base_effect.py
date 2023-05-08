from abc import ABCMeta


class BaseEffect(metaclass=ABCMeta):
    def __init__(self, holds_state) -> None:
        self.holds_state = holds_state

    def __format__(self, format_spec) -> str:
        if format_spec == "pp":
            return [("", self.__str__())]
        return self.__str__()
