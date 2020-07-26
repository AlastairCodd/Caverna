from abc import abstractmethod, ABCMeta


class Resettable(metaclass=ABCMeta):
    @abstractmethod
    def new_turn_reset(self) -> None:
        pass
