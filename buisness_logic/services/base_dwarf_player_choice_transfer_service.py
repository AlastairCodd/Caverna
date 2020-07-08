from abc import ABC, abstractmethod
from typing import List

from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.enums.harvest_type_enum import HarvestTypeEnum


class BaseDwarfPlayerChoiceTransferService(ABC):
    @abstractmethod
    def get_dwarf(
            self,
            player: Player,
            cards: List[BaseCard],
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) -> ResultLookup[Dwarf]:
        pass
