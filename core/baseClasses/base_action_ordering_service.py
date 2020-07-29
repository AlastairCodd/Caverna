from abc import ABCMeta, abstractmethod
from typing import List

from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from core.repositories.base_player_repository import BasePlayerRepository
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard


class ActionOrderingService(metaclass=ABCMeta):
    @abstractmethod
    def calculated_best_order(
            self,
            actions: ActionChoiceLookup,
            player: BasePlayerRepository,
            current_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[List[BaseAction]]:
        pass
