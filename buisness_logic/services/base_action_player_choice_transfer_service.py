from abc import ABCMeta, abstractmethod
from typing import List

from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from core.services.base_player_service import BasePlayerService
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.enums.harvest_type_enum import HarvestTypeEnum


class BaseActionPlayerChoiceTransferService(metaclass=ABCMeta):
    @abstractmethod
    def get_action(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            card: BaseCard,
            cards: List[BaseCard],
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) -> ResultLookup[ActionChoiceLookup]:
        pass
