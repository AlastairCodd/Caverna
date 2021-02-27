from typing import List, Tuple, Optional, Dict, Any

from PyInquirer import prompt, Separator

from buisness_logic.effects.food_effects import BaseFoodEffect
from buisness_logic.effects.purchase_effects import BaseTilePurchaseEffect
from common.defaults.tile_container_default import TileContainerDefault
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.tile_unknown_placement_lookup import TileUnknownPlacementLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_tile import BaseTile
from core.containers.resource_container import ResourceContainer
from core.enums.caverna_enums import ResourceTypeEnum
from core.services.base_player_service import BasePlayerService


class KeyboardHumanPlayerService(BasePlayerService):
    def __init__(self):
        BasePlayerService.__init__(
            self,
            0,
            0,
            TileContainerDefault())

    def get_player_choice_conversions_to_perform(
            self,
            turn_descriptor: TurnDescriptorLookup) -> List[Tuple[List[ResourceTypeEnum], int, List[ResourceTypeEnum]]]:
        pass

    def get_player_choice_weapon_level(
            self,
            turn_descriptor: TurnDescriptorLookup) -> int:
        pass

    def get_player_choice_animals_to_breed(
            self,
            animals_which_can_reproduce: List[ResourceTypeEnum],
            possible_number_of_animals_to_reproduce: int,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[List[ResourceTypeEnum]]:
        pass

    def get_player_choice_use_dwarf_out_of_order(
            self,
            dwarves: List[Dwarf],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[bool]:
        if dwarves is None:
            raise ValueError("Dwarves may not be None")
        name = "use_dwarf_out_of_order"
        question = [
            {'type': 'confirm',
             "message": "Use Dwarf out of Order?",
             "name": name,
             "default": False,}
        ]

        answer = prompt(question)
        result: ResultLookup[bool] = ResultLookup(answer[name],answer[name])
        return result

    def get_player_choice_use_card_already_in_use(
            self,
            unused_available_cards: List[BaseCard],
            used_available_cards: List[BaseCard],
            amount_of_food_required: int,
            turn_descriptor: TurnDescriptorLookup) -> bool:
        name = "use_card_already_in_use"
        question = [
            {'type': 'confirm',
             "message": "Use card already in use?",
             "name": name,
             "default": False,}
        ]

        answer = prompt(question)
        result: bool = answer[name]
        return result

    def get_player_choice_card_to_use(
            self,
            available_cards: List[BaseCard],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[BaseCard]:
        cards_by_name: Dict[str, BaseCard] = {card.name: card for card in available_cards}

        choices: Dict[str, Dict[str, Any]] = {}
        for card in available_cards:
            card_description: Dict[str, Any] = {}
            if card.actions is not None:
                card_description["Actions:"] = str(card.actions)
            if isinstance(card, ResourceContainer) and card.has_resources:
                displayable_resources: str = ", ".join([f"{resource.name}: {amount}" for resource, amount in card.resources.items()])
                card_description["Resources:"] = displayable_resources
            choices[card.name] = card_description
            print(card.name)
            print(card_description)
            print()

        name = "card_to_use"
        question = [
            {
                'type': 'list',
                'name': name,
                'message': 'Pick a card',
                'choices': choices
            },]

        answer = prompt(question)
        result: ResultLookup[BaseCard] = ResultLookup(True, cards_by_name[answer[name]])
        return result

    def get_player_choice_dwarf_to_use_out_of_order(
            self,
            dwarves: List[Dwarf],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[Dwarf]:
        name = "card_to_use"
        question = [
            {"type": "list",
             "message": "Pick a dwarf",
             "name": name,
             "choices": dwarves}
        ]

        answer = prompt(question)
        result: ResultLookup[Dwarf] = answer[name]
        return result

    def get_player_choice_actions_to_use(
            self,
            available_action_choices: List[ActionChoiceLookup],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        if available_action_choices is None:
            raise ValueError("Available Action Choices cannot be None")
        if not any(available_action_choices):
            raise ValueError("Must have at least one available choice")

        choices_by_string: Dict[str, ActionChoiceLookup] = {str(choice): choice for choice in available_action_choices}

        name = "actions_to_use"
        question = [
            {"type": "list",
             "message": "Choose some actions to use",
             "name": name,
             "choices": choices_by_string}
        ]

        answer = prompt(question)
        result: ResultLookup[ActionChoiceLookup] = ResultLookup(True, choices_by_string[answer[name]])
        return result

    def get_player_choice_tile_to_build(
            self,
            possible_tiles: List[BaseTile],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[BaseTile]:
        pass

    def get_player_choice_expedition_reward(
            self,
            possible_expedition_rewards: List[BaseAction],
            expedition_level: int,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[List[BaseAction]]:
        pass

    def get_player_choice_location_to_build(
            self,
            tile: BaseTile,
            turn_descriptor: TurnDescriptorLookup,
            secondary_tile: Optional[BaseTile] = None) -> ResultLookup[TileUnknownPlacementLookup]:
        pass

    def get_player_choice_location_to_build_stable(
            self,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[int]:
        pass

    def get_player_choice_effects_to_use_for_cost_discount(
            self,
            tile_cost: Dict[ResourceTypeEnum, int],
            turn_descriptor: TurnDescriptorLookup) -> Dict[BaseTilePurchaseEffect, int]:
        pass

    def get_player_choice_use_harvest_action_instead_of_breeding(
            self,
            turn_descriptor: TurnDescriptorLookup) -> bool:
        pass

    def get_player_choice_effect_to_use_for_feeding_dwarves(
            self,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[List[BaseFoodEffect]]:
        pass

    def get_player_choice_locations_to_sow(
            self,
            number_of_resources_to_sow: int,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[List[int]]:
        pass

    def get_player_choice_resources_to_sow(
            self,
            number_of_resources_to_sow: int,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[List[ResourceTypeEnum]]:
        pass
