from abc import ABCMeta, abstractmethod
from typing import List

from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.repositories.base_player_repository import BasePlayerRepository


class ActionOrderingService(metaclass=ABCMeta):
    @abstractmethod
    def calculate_best_order(
            self,
            actions: ActionChoiceLookup,
            player: BasePlayerRepository,
            current_card: BaseCard,
            current_dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[List[BaseAction]]:
        pass
