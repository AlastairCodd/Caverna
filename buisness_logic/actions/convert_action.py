from typing import Tuple, List

from buisness_logic.actions.convert_single_action import ConvertSingleAction
from buisness_logic.services.base_receive_event_service import BaseReceiveEventService
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.enums.caverna_enums import ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository
from core.services.base_player_service import BasePlayerService


class ConvertAction(BaseReceiveEventService, BasePlayerChoiceAction):
    def set_player_choice(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        if player is None:
            raise ValueError("Player may not be None")
        if turn_descriptor is None:
            raise ValueError("Turn Descriptor may not be none")

        conversions_to_perform: List[Tuple[List[ResourceTypeEnum], int, List[ResourceTypeEnum]]] = player\
            .get_player_choice_conversions_to_perform(turn_descriptor)

        convert_single_actions: List[ConvertSingleAction] = []
        for resources_to_be_converted, amount_of_resource_to_convert, resource_to_be_convert_into in conversions_to_perform:
            if amount_of_resource_to_convert == 0:
                continue
            convert_single_action: ConvertSingleAction = ConvertSingleAction(
                resources_to_be_converted,
                resource_to_be_convert_into,
                amount_of_resource_to_convert)
            convert_single_actions.append(convert_single_action)

        result: ResultLookup[ActionChoiceLookup] = ResultLookup(True, ActionChoiceLookup(convert_single_actions))
        return result

    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        result = ResultLookup(True, 0)
        return result

    def new_turn_reset(self) -> None:
        pass
