from abc import abstractmethod, ABC

from common.entities.dwarf import Dwarf
from core.containers.resource_container import ResourceContainer


class BaseAction(ABC):

    @abstractmethod
    def invoke(self, player: 'Player', active_card: 'BaseCard', current_dwarf: Dwarf) -> bool:
        raise NotImplementedError("abstract base action class")

    @abstractmethod
    def new_turn_reset(self):
        pass
