from typing import NamedTuple, Tuple, Dict, Optional, TypeVar, Callable

from buisness_logic.cards.imitation_card import ImitationCard
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.constants import game_constants
from core.services.base_action_choice_processor_service import BaseActionChoiceProcessorService


class CardActionChoice(NamedTuple):
    index: int
    card_id: int


class ActionsAndConstraintsActionChoice(NamedTuple):
    index: int
    actions: ActionChoiceLookup


class UseDwarfOutOfOrderActionChoice(NamedTuple):
    index: int
    should_use_dwarf_out_of_order: bool


class DwarfToUseOutOfOrder(NamedTuple):
    index: int
    dwarf_id: int


T = TypeVar('T')


class CardActionChoiceProcessorService(BaseActionChoiceProcessorService):
    def __init__(self) -> None:
        self._card_choices: Dict[int, CardActionChoice]
        self._action_choices: Dict[int, ActionsAndConstraintsActionChoice]
        self._use_dwarf_out_of_order_choices: Dict[int, UseDwarfOutOfOrderActionChoice]
        self._dwarf_to_use_out_of_order_choices: Dict[int, Optional[DwarfToUseOutOfOrder]]

        self._card_choices, self._action_choices,\
            self._use_dwarf_out_of_order_choices, self._dwarf_to_use_out_of_order_choices = self._populate_choices()

        BaseActionChoiceProcessorService.__init__(self, len(self._card_choices))

    def process_action_choice_card(self) -> CardActionChoice:
        return self._process_action(self.convert_index_to_card_choice)

    def process_action_choice_action(self) -> ActionsAndConstraintsActionChoice:
        return self._process_action(self.convert_index_to_action_choice)

    def process_action_choice_use_dwarf_out_of_order(self) -> UseDwarfOutOfOrderActionChoice:
        return self._process_action(self.convert_index_to_use_dwarf_out_of_order_choice)

    def process_action_choice_dwarf_to_use(self) -> DwarfToUseOutOfOrder:
        return self._process_action(self.convert_index_to_dwarf_choice)

    def convert_index_to_card_choice(self, index: int) -> CardActionChoice:
        return self._card_choices[index]

    def convert_index_to_action_choice(self, index: int) -> ActionsAndConstraintsActionChoice:
        return self._action_choices[index]

    def convert_index_to_use_dwarf_out_of_order_choice(self, index: int) -> UseDwarfOutOfOrderActionChoice:
        return self._use_dwarf_out_of_order_choices[index]

    def convert_index_to_dwarf_choice(self, index: int) -> DwarfToUseOutOfOrder:
        return self._dwarf_to_use_out_of_order_choices[index]

    def _process_action(
            self,
            index_conversion_func: Callable[[int], T]) -> T:
        probabilities: list[Tuple[int, float]] = self._get_action_choice_subset(self._length)

        for index, probability in probabilities:
            if index in self._invalid_actions:
                continue
            return index_conversion_func(index)
        raise IndexError("No valid choices")

    def _populate_choices(self) -> Tuple[
            Dict[int, CardActionChoice],
            Dict[int, ActionsAndConstraintsActionChoice],
            Dict[int, UseDwarfOutOfOrderActionChoice],
            Dict[int, Optional[DwarfToUseOutOfOrder]]
    ]:
        from buisness_logic.actions.go_on_an_expedition_action import GoOnAnExpeditionAction
        from buisness_logic.actions.give_dwarf_a_weapon_action import GiveDwarfAWeaponAction
        from buisness_logic.effects.action_effects import ChangeDecisionVerb, ActionCombinationEnum
        from common.entities.action_choice_lookup import ActionChoiceLookup
        from common.forges.card_forge_complete import CompleteCardForge
        from common.services.conditional_service import ConditionalService

        complete_card_forge: CompleteCardForge = CompleteCardForge()
        conditional_service: ConditionalService = ConditionalService()
        change_decision_effects: list[ChangeDecisionVerb] = [ChangeDecisionVerb(ActionCombinationEnum.EitherOr, ActionCombinationEnum.AndOr)]

        all_cards: Dict[int, BaseCard] = complete_card_forge.get_cards()

        index: int = 0
        card_choices: Dict[int, CardActionChoice] = {}
        action_choices: Dict[int, ActionsAndConstraintsActionChoice] = {}
        use_dwarf_out_of_order_choices: Dict[int, UseDwarfOutOfOrderActionChoice] = {}
        dwarf_to_use_out_of_order_choices: Dict[int, Optional[DwarfToUseOutOfOrder]] = {}

        items = sorted(all_cards.items(), key=lambda kvp: kvp[0])
        for card_id, card in items:
            if isinstance(card, ImitationCard):
                continue
            card_action_conditional: Conditional = card.actions
            possible_action_choices: list[ActionChoiceLookup] = conditional_service.get_possible_choices(card_action_conditional, change_decision_effects)

            for action_choice in possible_action_choices:
                card_choices[index] = CardActionChoice(index, card.id)
                action_choices[index] = ActionsAndConstraintsActionChoice(index, action_choice)
                use_dwarf_out_of_order_choices[index] = UseDwarfOutOfOrderActionChoice(index, False)
                dwarf_to_use_out_of_order_choices[index] = None
                index += 1

                any_expedition_actions: bool = any(action for action in action_choice.actions if isinstance(action, GoOnAnExpeditionAction))
                if any_expedition_actions:
                    any_give_dwarf_a_weapon_actions: bool = any(action for action in action_choice.actions if isinstance(action, GiveDwarfAWeaponAction))
                    if not any_give_dwarf_a_weapon_actions:
                        for i in range(game_constants.maximum_number_of_dwarves):
                            card_choices[index] = CardActionChoice(index, card.id)
                            action_choices[index] = ActionsAndConstraintsActionChoice(index, action_choice)
                            use_dwarf_out_of_order_choices[index] = UseDwarfOutOfOrderActionChoice(index, True)
                            dwarf_to_use_out_of_order_choices[index] = DwarfToUseOutOfOrder(index, i)
                            index += 1

        return card_choices, action_choices, use_dwarf_out_of_order_choices, dwarf_to_use_out_of_order_choices
