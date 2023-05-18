from abc import ABCMeta
from typing import Dict

from buisness_logic.actions.check_animal_storage_action import CheckAnimalStorageAction
from buisness_logic.services.base_receive_event_service import BaseReceiveEventService
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.precedes_constraint import PrecedesConstraint
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_constraint import BaseConstraint
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.constants import resource_types
from core.enums.caverna_enums import ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository


class BaseReceiveAction(BasePlayerChoiceAction, BaseReceiveEventService, metaclass=ABCMeta):
    def __init__(
            self,
            name: str,
            items_to_receive: Dict[ResourceTypeEnum, int]):
        if items_to_receive is None:
            raise ValueError("Items to Receive cannot be None")
        self._items_to_receive: Dict[ResourceTypeEnum] = items_to_receive
        BaseAction.__init__(self, name, True, False, False)

    def set_player_choice(
            self,
            player: BasePlayerRepository,
            dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        action_choice: ActionChoiceLookup
        if any(map(lambda animal: animal in self._items_to_receive, resource_types.farm_animals)):
            action: BaseAction = CheckAnimalStorageAction()
            precedes_constraint: BaseConstraint = PrecedesConstraint(self, action)
            action_choice = ActionChoiceLookup([action], [precedes_constraint])
        else:
            action_choice = ActionChoiceLookup([])
        result: ResultLookup[ActionChoiceLookup] = ResultLookup(True, action_choice)
        return result
