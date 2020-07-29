from abc import ABCMeta, abstractmethod
from typing import List

from common.entities.dwarf import Dwarf
from core.services.base_player_service import BasePlayerService
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.enums.harvest_type_enum import HarvestTypeEnum


class BaseDwarfPlayerChoiceTransferService(metaclass=ABCMeta):
    @abstractmethod
    def get_dwarf(
            self,
            player: BasePlayerService,
            cards: List[BaseCard],
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) -> ResultLookup[Dwarf]:
        pass
