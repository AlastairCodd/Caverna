from abc import abstractmethod, ABCMeta

from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_action import BaseAction
from core.services.base_player_service import BasePlayerService


class BasePlayerChoiceAction(BaseAction, metaclass=ABCMeta):
    @abstractmethod
    def set_player_choice(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        raise NotImplementedError("abstract base player choice action class")
