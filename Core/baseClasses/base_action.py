from abc import abstractmethod, ABC

from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.services.resettable import Resettable


class BaseAction(ABC, Resettable):

    @abstractmethod
    def invoke(self, player: 'Player', active_card: 'BaseCard', current_dwarf: Dwarf) -> ResultLookup[int]:
        raise NotImplementedError("abstract base action class")
