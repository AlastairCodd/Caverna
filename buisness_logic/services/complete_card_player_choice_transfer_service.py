from typing import List, Optional, Tuple

from buisness_logic.actions.activate_dwarf_action import ActivateDwarfAction
from buisness_logic.actions.pay_action import PayAction
from buisness_logic.cards.imitation_card import ImitationCard
from buisness_logic.services.available_card_service import AvailableCardService
from buisness_logic.services.base_card_player_choice_transfer_service import BaseCardPlayerChoiceTransferService
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum
from core.services.base_player_service import BasePlayerService


class CompleteCardPlayerChoiceTransferService(BaseCardPlayerChoiceTransferService):
    def __init__(self):
        self._available_card_service: AvailableCardService = AvailableCardService()

    def get_card(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[Tuple[BaseCard, ActionChoiceLookup]]:
        if player is None:
            raise ValueError("Player cannot be null")
        if dwarf is None:
            raise ValueError("Dwarf cannot be null")

        success: bool = True
        errors: List[str] = []

        unused_available_cards: List[BaseCard] = self._available_card_service.get_cards_which_are_free_to_use(turn_descriptor.cards)
        used_available_cards: List[BaseCard] = self._available_card_service.get_cards_which_are_used_by_someone_else(turn_descriptor.cards, player)

        can_use_card_already_in_use_result: ResultLookup[bool] = self._available_card_service.can_use_card_already_in_use(
            unused_available_cards,
            used_available_cards)

        use_card_already_in_use: bool = False
        imitation_card: Optional[ImitationCard] = None
        if can_use_card_already_in_use_result.flag:
            imitation_card_result: ResultLookup[ImitationCard] = self._available_card_service.get_imitation_card(unused_available_cards)

            success &= imitation_card_result.flag
            errors.extend(imitation_card_result.errors)

            if imitation_card_result.flag:
                imitation_card: ImitationCard = imitation_card_result.value

                use_card_already_in_use: bool = player.get_player_choice_use_card_already_in_use(
                    unused_available_cards,
                    used_available_cards,
                    imitation_card.amount_of_food,
                    turn_descriptor)

        additional_actions: List[BaseAction] = []

        card_choice_result: ResultLookup[BaseCard]
        if use_card_already_in_use:
            card_choice_result = player.get_player_choice_card_to_use(
                used_available_cards,
                turn_descriptor)

            if imitation_card.amount_of_food > 0:
                take_food_action: BaseAction = PayAction({ResourceTypeEnum.food: imitation_card.amount_of_food})
                additional_actions.append(take_food_action)

            activate_dwarf_action: BaseAction = ActivateDwarfAction(imitation_card)
            additional_actions.append(activate_dwarf_action)
        else:
            card_choice_result = player.get_player_choice_card_to_use(
                unused_available_cards,
                turn_descriptor)
            activate_dwarf_action: BaseAction = ActivateDwarfAction()
            additional_actions.append(activate_dwarf_action)

        success &= card_choice_result.flag
        errors.extend(card_choice_result.errors)

        result: ResultLookup[Tuple[BaseCard, ActionChoiceLookup]]
        if success:
            action_choice: ActionChoiceLookup = ActionChoiceLookup(additional_actions, [])
            result = ResultLookup(True, (card_choice_result.value, action_choice), errors)
        else:
            result = ResultLookup(errors=errors)
        return result
