from abc import abstractmethod, ABCMeta

from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.services.resettable import Resettable
from core.repositories.base_player_repository import BasePlayerRepository


# noinspection PyUnresolvedReferences
class BaseAction(Resettable, metaclass=ABCMeta):
    def __init__(self, name: str) -> None:
        self._name: str = name

    @abstractmethod
    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: 'BaseCard',
            current_dwarf: Dwarf) -> ResultLookup[int]:
        raise NotImplementedError("abstract base action class")

    @property
    def name(self) -> str:
        return self._name

    def __format__(self, format_spec) -> str:
        return str(self)

    @abstractmethod
    def __hash__(self) -> int:
        raise NotImplemented()
