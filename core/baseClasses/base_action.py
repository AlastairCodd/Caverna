from abc import abstractmethod, ABCMeta

from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.services.resettable import Resettable
from core.repositories.base_player_repository import BasePlayerRepository


# noinspection PyUnresolvedReferences
class BaseAction(Resettable, metaclass=ABCMeta):
    def __init__(
            self,
            name: str,
            mutates_player: bool,
            mutates_card: bool,
            mutates_dwarf: bool) -> None:
        self._name: str = name
        self._mutates_player = mutates_player
        self._mutates_card = mutates_card
        self._mutates_dwarf = mutates_dwarf

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

    @property
    def mutates_player(self) -> bool:
        return self._mutates_player

    @property
    def mutates_card(self) -> bool:
        return self._mutates_card

    @property
    def mutates_dwarf(self) -> bool:
        return self._mutates_dwarf

    def __format__(self, format_spec) -> str:
        return str(self)

    @abstractmethod
    def __hash__(self) -> int:
        raise NotImplemented()
