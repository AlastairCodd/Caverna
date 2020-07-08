from abc import ABC, abstractmethod


class Resettable(ABC):
    @abstractmethod
    def new_turn_reset(self):
        pass
