from abc import abstractmethod, ABCMeta
from typing import List

from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.enums.harvest_type_enum import HarvestTypeEnum


class BasePlayerChoiceAction(BaseAction, metaclass=ABCMeta):
    # TODO: What if this is immitated?
    @abstractmethod
    def set_player_choice(
            self,
            player: Player,
            dwarf: Dwarf,
            cards: List[BaseCard],
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) -> ResultLookup[ActionChoiceLookup]:
        raise NotImplementedError("abstract base player choice action class")
