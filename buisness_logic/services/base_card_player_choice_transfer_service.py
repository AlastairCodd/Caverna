from abc import ABCMeta, abstractmethod
from typing import Tuple

from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_card import BaseCard
from core.services.base_player_service import BasePlayerService


class BaseCardPlayerChoiceTransferService(metaclass=ABCMeta):
    @abstractmethod
    def get_card(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[Tuple[BaseCard, ActionChoiceLookup]]:
        pass
