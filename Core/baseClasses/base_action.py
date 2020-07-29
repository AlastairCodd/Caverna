from abc import abstractmethod, ABCMeta

from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.services.resettable import Resettable
from core.repositories.base_player_repository import BasePlayerRepository


class BaseAction(Resettable, metaclass=ABCMeta):
    @abstractmethod
    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: 'BaseCard',
            current_dwarf: Dwarf) -> ResultLookup[int]:
        raise NotImplementedError("abstract base action class")
