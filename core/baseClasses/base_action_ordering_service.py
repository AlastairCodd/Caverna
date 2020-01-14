from abc import ABC, abstractmethod
from typing import List

from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard


class ActionOrderingService(ABC):
    @abstractmethod
    def calculated_best_order(
            self,
            actions: ActionChoiceLookup,
            player: Player,
            current_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[List[BaseAction]]:
        pass
