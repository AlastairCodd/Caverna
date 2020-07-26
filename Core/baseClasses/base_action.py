from abc import abstractmethod, ABCMeta

from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.services.resettable import Resettable


class BaseAction(Resettable, metaclass=ABCMeta):
    @abstractmethod
    def invoke(
            self,
            player: 'Player',
            active_card: 'BaseCard',
            current_dwarf: Dwarf) -> ResultLookup[int]:
        raise NotImplementedError("abstract base action class")
