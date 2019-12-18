from abc import abstractmethod, ABC

from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from core.containers.resource_container import ResourceContainer


class BaseAction(ABC):

    @abstractmethod
    def invoke(self, player: 'Player', active_card: 'BaseCard', current_dwarf: Dwarf) -> ResultLookup[int]:
        raise NotImplementedError("abstract base action class")

    @abstractmethod
    def new_turn_reset(self):
        pass
