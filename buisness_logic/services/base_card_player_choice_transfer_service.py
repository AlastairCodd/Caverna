from abc import ABCMeta, abstractmethod
from typing import List

from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.enums.harvest_type_enum import HarvestTypeEnum


class BaseCardPlayerChoiceTransferService(metaclass=ABCMeta):
    @abstractmethod
    def get_card(
            self,
            player: Player,
            dwarf: Dwarf,
            cards: List[BaseCard],
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) -> ResultLookup[BaseCard]:
        pass
