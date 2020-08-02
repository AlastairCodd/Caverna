from abc import ABCMeta, abstractmethod

from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.services.base_player_service import BasePlayerService


class BaseDwarfPlayerChoiceTransferService(metaclass=ABCMeta):
    @abstractmethod
    def get_dwarf(
            self,
            player: BasePlayerService,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[Dwarf]:
        pass
