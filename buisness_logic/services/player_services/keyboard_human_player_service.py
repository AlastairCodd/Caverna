import math
from enum import Enum
from shutil import get_terminal_size
from textwrap import wrap
from typing import List, Tuple, Optional, Dict, Any, Union, Callable

from InquirerPy.utils import patched_print
from InquirerPy.utils import color_print
from InquirerPy import inquirer, prompt

from buisness_logic.actions.receive_action import ReceiveAction
from buisness_logic.effects.conversion_effects import ConvertEffect
from buisness_logic.effects.food_effects import BaseFoodEffect
from buisness_logic.effects.free_action_effects import FreeActionEffect
from buisness_logic.effects.purchase_effects import BaseTilePurchaseEffect
from common.defaults.tile_container_default import TileContainerDefault
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.resources_to_sow_lookup import ResourcesToSow
from common.entities.result_lookup import ResultLookup
from common.entities.tile_twin_placement_lookup import TileTwinPlacementLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from common.services.tile_service import LocationValidity, ValidLocations, TwinLocationValidity
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_tile import BaseTile
from core.containers.resource_container import ResourceContainer
from core.enums.caverna_enums import ResourceTypeEnum, TileTypeEnum
from core.services.base_player_service import BasePlayerService, InvalidActionCombinationResponse


FormattedText = List[Tuple[str, str]]
Styles = Dict[str, str]
Printable = str | Tuple[FormattedText, Optional[Styles]]


def append_resources(
        text: FormattedText,
        resources: Dict[ResourceTypeEnum, int],
        if_empty: Optional[Callable[[FormattedText], None]]) -> None:
    if len(resources) == 0 or all(amount == 0 for amount in resources.values()):
        if if_empty is not None:
            if_empty(text)
        return

    for (i, (resource, amount)) in enumerate(resources.items()):
        text.append(("class:count", str(amount)))
        text.append(("", " "))
        text.append(("class:resource", resource.name))
        if i < len(resources) - 1:
            text.append(("", ", "))

def wrap_styled_text_to_fit_current_terminal(
        text: FormattedText,
        amount_to_indent_by: int = 0) -> FormattedText:
    terminal_width = get_terminal_size().columns
    number_of_new_elements = 0
    for (i, (style, styled_element)) in enumerate(text):
        wrapped: List[str] = wrap(
            styled_element,
            terminal_width,
            subsequent_indent=' ' * amount_to_indent_by)
        if len(wrapped) == 1:
            continue
        for (j, wrapped_element) in enumerate(wrapped):
            text[i + number_of_new_elements + j] = (style, wrapped_element)
        number_of_new_elements += len(wrapped)
    return text


class TilePlacementOptions:
    def __init__(self) -> None:
        self.needs_clean = True
        self.ignore_adjacency = False
        self.ignore_requisites = False


class KeyboardHumanPlayerService(BasePlayerService):
    def __init__(
            self,
            player_id: int,
            player_descriptor: str,
            player_turn_index: int) -> None:
        BasePlayerService.__init__(
            self,
            player_id,
            player_descriptor,
            player_turn_index,
            TileContainerDefault())

    def report_action_choice_failed(
            self,
            actions) -> InvalidActionCombinationResponse:
        choices_and_text: Dict[InvalidActionCombinationResponse, str] = {
                InvalidActionCombinationResponse.ResetEntireChoice: "Make entirely different choices",
                InvalidActionCombinationResponse.UseDifferentDwarf: "Change which dwarf to use",
                InvalidActionCombinationResponse.PickCardAgain: "Pick a different card",
                InvalidActionCombinationResponse.MakeDifferentCardChoice: "Choose different card actions",
                InvalidActionCombinationResponse.ChooseDifferentOptionsInActions: "Make different choices for actions",
                InvalidActionCombinationResponse.TryDifferentConversions: "Choose different conversions",
                InvalidActionCombinationResponse.StopTryingToPerformSomeFreeActions: "Choose different free actions",
        }

        choices: List[Dict[str, Any]] = [{'value': k, 'name': v} for (k, v) in choices_and_text.items()]

        choice: InvalidActionCombinationResponse = inquirer.select(
            message="The chosen actions cannot be performed",
            choices=choices
        ).execute()

        return choice

    def get_player_choice_conversions_to_perform(
            self,
            turn_descriptor: TurnDescriptorLookup) -> List[Tuple[List[ResourceTypeEnum], int, List[ResourceTypeEnum]]]:
        wishes_to_convert_anything_into_food = inquirer.confirm(message="Would you like to convert any resources into food?").execute()

        if not wishes_to_convert_anything_into_food:
            return []
        possible_resources_to_convert_into_food: Dict[ResourceTypeEnum, List[Tuple[int, ConvertEffect]]] = {}
        other_food_conversion_effects: List[ConvertEffect] = []
        for convert_effect in self.get_effects_of_type(ConvertEffect):
            if ResourceTypeEnum.food not in convert_effect.output:
                continue
            if len(convert_effect.input) > 1:
                raise NotImplementedError("Do not currently support converting from multiple different input into food")
                #other_food_conversion_effects.append(convert_effect)
                #continue
            input_resource: ResourceTypeEnum
            number_of_input_to_convert: int
            input_resource, number_of_input_to_convert = next(iter(convert_effect.input.items()))
            effects_for_input = possible_resources_to_convert_into_food \
                .get(input_resource, [])
            effects_for_input.append((number_of_input_to_convert, convert_effect))
            possible_resources_to_convert_into_food[input_resource] = effects_for_input

        food_conversion_choices: List[Dict[str, Any]] = []
            #{'name': ", ".join(resource.name for resource in convert_effect.input),
            # 'value': convert_effect}
            #for convert_effect in other_food_conversion_effects]

        food_conversion_choices.extend(
            {'name': f"{resource.name}",
             'value': counts[0][1]}
            for (resource, counts) in possible_resources_to_convert_into_food.items()
            if len(counts) == 1)

        food_conversion_choices.extend(
            {'name': f"{resource.name} (" + ", ".join(f"x{count}" for (count, _) in counts) + ")",
             'value': [effect for (_, effect) in counts]}
            for (resource, counts) in possible_resources_to_convert_into_food.items()
            if len(counts) > 1)

        chosen_food_conversions = inquirer.checkbox(
            message="Pick conversions to perform",
            long_instruction="Use 'space' to select conversions to perform",
            choices=food_conversion_choices).execute()

        conversions_to_perform: List[Tuple[List[ResourceTypeEnum], int, List[ResourceTypeEnum]]] = []
        for conversion in chosen_food_conversions:
            if isinstance(conversion, ConvertEffect):
                input_resource: ResourceTypeEnum = next(iter(conversion.input))
                number_of_conversions_to_perform = inquirer.number(
                    message=f"How many of the input ({input_resource.name}) would you like to convert?",
                    filter=lambda result: int(result)).execute()
                if number_of_conversions_to_perform <= 0:
                   continue
                conversions_to_perform.append((
                    [input_resource],
                    number_of_conversions_to_perform,
                    [ResourceTypeEnum.food]))
            else:
                # inputs are currently guaranteed to all be equivalent, excepting count, due to exception above
                #    which asserts that only one input is permitted
                effects: List[ConversionEffect] = conversion
                # grab from a random conversion
                input_resource: ResourceTypeEnum = next(iter(effects[0].input))
                minimal_amount_of_input_resource = min(effect.input[input_resource] for effect in effects)
                number_of_conversions_to_perform = inquirer.number(
                    message=f"How many of the input ({input_resource.name}) would you like to convert?",
                    filter=lambda result: int(result) if result is not None else 0,
                    # this could be better, by allowing spin down to zero and only validating that number
                    min_allowed=minimal_amount_of_input_resource,
                    raise_keyboard_interrupt=False,
                    mandatory=False).execute()
                if number_of_conversions_to_perform <= 0:
                   continue
                conversions_to_perform.append((
                    [input_resource],
                    number_of_conversions_to_perform,
                    [ResourceTypeEnum.food]))
        patched_print(conversions_to_perform)
        return conversions_to_perform

    def get_player_choice_market_items_to_purchase(
            self,
            purchasable_items: Dict[ResourceTypeEnum, int],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[List[ResourceTypeEnum]]:
        choices: List[Dict[str, Any]] = [
            {'name': f"{reward.name} ({cost})",
             'value': reward}
             for (reward, cost) in purchasable_items.items()]

        chosen_purchases_prompt = inquirer.checkbox(
             message="Pick market items to buy",
             choices=choices)

        @chosen_purchases_prompt.register_kb("t")
        def _handle_total(event):
            total_cost: int = 0
            chosen_items: List[ResourceTypeEnum] = chosen_purchases_prompt.result_value

            text = [("", "total cost of ")]
            for (i, reward) in enumerate(chosen_items):
                total_cost += purchasable_items[cost]
                text.append(("class:resource", resource.name))
                if i == len(chosen_items) - 1:
                    continue
                if i == len(chosen_items) - 2:
                    text.append(("", " and "))
                    continue
                text.append(("", ", "))
            text.append(("", " is "))
            text.append(("class:cost", total_cost))

            # FIXME: this is a pretty long message, would benefit from being forced to multilines
            color_print(text, style={"count": "yellow"})
            _warn_if_total_cost_is_more_than_expected_allowed(total_cost)

        self._add_keybinding_that_shows_resources(chosen_purchases_prompt)

        def _warn_if_total_cost_of_purchases_is_more_than_expected_allowed(
                purchases: List[ResourceTypeEnum]) -> None:
            total_cost: int = sum(purchasable_items[resource] for resource in chosen_rewards)
            _warn_if_total_cost_is_more_than_expected_allowed(total_cost)

        def _warn_if_total_cost_is_more_than_expected_allowed(
                total_cost: int) -> None:
            expected_budget: int = self.get_resources_of_type(ResourceTypeEnum.coin) + 4
            if total_cost <= expected_budget:
                return
            # cost of currently selected items is 4, and anticipated amount of coins available (without performing any conversions) is only 4
            warning = [
                ("class:warning", "cost of currently chosen market items is "),
                ("class:count", str(total_cost)),
                ("class:warning", " and anticipated amount of coins available "),
                ("class:aside", "(assuming no conversions are performed) "),
                ("class:warning", "is only "),
                ("class:count", str(expected_budget)),
            ]
            color_print(warning, style={"warning": "red", "count": "yellow", "aside": "italic"})

        chosen_rewards: List[ResourceTypeEnum] = chosen_purchases_prompt.execute()

        _warn_if_total_cost_of_purchases_is_more_than_expected_allowed(chosen_rewards)

        result: ResultLookup[List[ResourceTypeEnum]] = ResultLookup(True, chosen_rewards)
        return result

    def get_player_choice_weapon_level(
            self,
            turn_descriptor: TurnDescriptorLookup) -> int:
        weapon_level_prompt = inquirer.number(
            message="How much ore would you like to spend on equipping your dwarf with a weapon?",
            min_allowed=1,
            max_allowed=8)
        self._add_keybinding_that_shows_resources(weapon_level_prompt)

        return int(weapon_level_prompt.execute())

    def get_player_choice_animals_to_breed(
            self,
            animals_which_can_reproduce: List[ResourceTypeEnum],
            possible_number_of_animals_to_reproduce: int,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[List[ResourceTypeEnum]]:
        return ResultLookup(True, [])

    def get_player_choice_use_dwarf_out_of_order(
            self,
            dwarves: List[Dwarf],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[bool]:
        if dwarves is None:
            raise ValueError("Dwarves may not be None")

        use_dwarf_out_of_order = inquirer.confirm(
            "Use Dwarf out of Order?",
            default=False).execute()

        result: ResultLookup[bool] = ResultLookup(True, use_dwarf_out_of_order)
        return result

    def get_player_choice_use_card_already_in_use(
            self,
            unused_available_cards: List[BaseCard],
            used_available_cards: List[BaseCard],
            amount_of_food_required: int,
            turn_descriptor: TurnDescriptorLookup) -> bool:

        result = None
        first_loop = True
        while result is None:
            prompt = inquirer.confirm(
                message="Use card already in use?",
                instruction="(y/N/q)" if first_loop else "(y/N)",
                default=False,
                mandatory=not first_loop)

            if first_loop:
                @prompt.register_kb("q")
                def _handle_question(event):
                    print("\r\nCards which are already in use:")
                    for card in used_available_cards:
                        print(card.name)
                        print(f"    {card.actions:4}")
                    print()
                    print(f"(immitating a card costs {amount_of_food_required} food)")
                    print(f"(Harvest Phase at end of turn: {turn_descriptor.harvest_type.name})")
                    prompt._handle_skip(event)

            result = prompt.execute()
            first_loop = False

        return result

    def get_player_choice_card_to_use(
            self,
            available_cards: List[BaseCard],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[BaseCard]:
        choices: List[Dict[str, Any]] = [
            {'name': card.name,
             'value': card}
            for card in available_cards
        ]

        has_picked_card: bool = False

        while not has_picked_card:
            card_question = inquirer.select(
                message="Pick a card",
                choices=choices
            )

            self._add_keybinding_that_shows_resources(card_question)

            card_to_use: BaseCard = card_question.execute()

            newline_separator = "\r\n"
            card_description = [
                ("", "Confirm that you'd like to use "),
                ("class:identifier", card_to_use.name),
                ("", "?"),
                ("", newline_separator),
            ]
            if card_to_use.actions is not None:
                card_description.append(("", "  Actions:"))
                card_description.append(("", f"{newline_separator}    "))
                card_description.extend(card_to_use.actions.__format__("4pp"))
            if isinstance(card_to_use, ResourceContainer) and card_to_use.has_resources:
                card_description.append(("", f"{newline_separator}  "))
                card_description.append(("", "Resources: "))
                card_description.append(("", f"{newline_separator}    "))
                append_resources(card_description, card_to_use.resources, None)

            wrap_styled_text_to_fit_current_terminal(card_description, 6)
            color_print(card_description, style={"count": "yellow"})

            pick_card_question = inquirer.confirm(message="", default=True)
            self._add_keybinding_that_shows_resources(pick_card_question)

            has_picked_card = pick_card_question.execute()

        result: ResultLookup[BaseCard] = ResultLookup(True, card_to_use)
        return result

    def get_player_choice_dwarf_to_use_out_of_order(
            self,
            dwarves: List[Dwarf],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[Dwarf]:
        choices: List[Dict[str, Any]] = [
            {"name": dwarf.weapon_level,
             "value": dwarf}
            for dwarf in dwarves
        ]

        dwarf_to_use = inquirer.select(
            "Pick a Dwarf",
            choices=choices).execute()

        result: ResultLookup[Dwarf] = ResultLookup(True, dwarf_to_use)
        return result

    def get_player_choice_actions_to_use(
            self,
            available_action_choices: List[ActionChoiceLookup],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        if available_action_choices is None:
            raise ValueError("Available Action Choices cannot be None")
        if not any(available_action_choices):
            raise ValueError("Must have at least one available choice")

        choices: List[Dict[str, Any]] = [
            {"name": str(choice),
             "value": choice, }
            for choice in available_action_choices]

        actions_to_use = inquirer.select(
            message="Choose some actions to use",
            choices=choices).execute()

        result: ResultLookup[ActionChoiceLookup] = ResultLookup(True, actions_to_use)
        return result

    def get_player_choice_free_actions_to_use(
            self,
            turn_descriptor: TurnDescriptorLookup) -> List[BaseAction]:
        prompt = inquirer.confirm(
            message="Use any free actions?", 
            default=False)
        self._add_keybinding_that_shows_resources(prompt)
        if not prompt.execute():
            return []

        choices: List[Dict[str, Any]] = [
            {"name": str(effect.action),
             "value": effect.action, }
            for effect in self.get_effects_of_type(FreeActionEffect)]

        actions_to_use = inquirer.checkbox(
            message="Choose some actions to use",
            choices=choices).execute()

        return actions_to_use

    def get_player_choice_fences_to_build(
            self,
            place_pasture_action: BaseAction,
            place_twin_pasture_action: BaseAction,
            place_stable_action: Optional[BaseAction],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[List[BaseAction]]:
        if place_pasture_action is None:
            raise ValueError("place_pasture_action")
        if place_twin_pasture_action is None:
            raise ValueError("place_twin_pasture_action")

        choices = [place_pasture_action, place_twin_pasture_action]
        if place_stable_action is not None:
            choices.append(place_stable_action)

        prompt = inquirer.checkbox(
            message="Which fields would you like to build?",
            choices=choices)

        self._add_keybinding_that_shows_resources(prompt)
        self._add_keybinding_that_shows_round_info(prompt, turn_descriptor)

        return ResultLookup(True, prompt.execute())

    def get_player_choice_tile_to_build(
            self,
            possible_tiles: List[BaseTile],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[BaseTile]:
        if possible_tiles is None:
            raise ValueError("Possible Tiles cannot be None")
        if len(possible_tiles) == 0:
            raise ValueError("Possible Tiles cannot be empty")
        from buisness_logic.tiles.point_tiles import BaseConditionalPointTile

        prompt = inquirer.select(
            message="Pick a tile to build",
            choices=[
                {"name": tile.name,
                 "value": tile}
                for tile in possible_tiles
            ],
            instruction="Use ↑/↓ to pick the tile",
            long_instruction="'c' shows the cost of the currently selected tile, 'd' shows a description of its effects, 'r' to see current resources"
        )

        prompt.last_tile_to_show_cost = None

        @prompt.register_kb("c")
        def _handle_cost(event):
            current_tile = prompt.result_value
            if prompt.last_tile_to_show_cost == current_tile:
                return
            prompt.last_tile_to_show_cost = current_tile
            text = [("", "  "), ("", current_tile.name), ("", " costs: ")]

            append_resources(text, current_tile.cost, lambda text: text.append(("", "nothing")))
            color_print(text, style={"count": "yellow"})

        prompt.last_tile_to_show_description = None

        @prompt.register_kb("d")
        def _handle_description(event):
            current_tile = prompt.result_value
            if prompt.last_tile_to_show_description == current_tile:
                return
            prompt.last_tile_to_show_description = current_tile
            text = [
                ("", "  "),
                ("", f"{current_tile.name} ("),
                (f"class:{current_tile.colour.name.lower()}", "◆"),
                ("", ")"),
            ]

            any_effects = any(current_tile.effects)
            if any_effects:
                text.append(("", " has effects: "))
                for (i, effect) in enumerate(current_tile.effects):
                    formatted = effect.__format__("pp")
                    if isinstance(formatted, str):
                        patched_print(f"format for {effect!r} returned string")
                        text.append(("", formatted))
                    elif formatted is not None:
                        text.extend(formatted)
                    else:
                        patched_print(f"format for {effect!r} invalid")
                        text.append(("", repr(effect)))
                    if i < len(current_tile.effects) - 1:
                        text.append(("", ", "))

            if current_tile.base_points > 0:
                if any_effects:
                    text.append(("", "; and"))
                text.append(("", " is worth "))
                text.append(("class:point_count", str(current_tile.base_points)))
                text.append(("", " points unconditionally" if current_tile.base_points > 1 else " point unconditionally"))
                # cannot be both a conditional point tile and have base points
            elif isinstance(current_tile, BaseConditionalPointTile):
                if any_effects:
                    text.append(("", "; and"))
                text.append(("", " "))
                current_tile.append_formatted_conditional_points(text)
            text.append(("", "."))

            color_print(
                text,
                style={
                    "count": "yellow",
                    "point_count": "#61afef",
                    "green": "#90aa86",
                    "yellow": "#ff9f1c",
                    "brown": "#6f1a07"
                }
            )

        self._add_keybinding_that_shows_resources(prompt)

        tile_to_build = prompt.execute()

        result: ResultLookup[BaseTile] = ResultLookup(tile_to_build is not None, tile_to_build)
        return result

    def get_player_choice_expedition_reward(
            self,
            possible_expedition_rewards: List[Tuple[BaseAction, int]],
            expedition_level: int,
            is_first_expedition_action: bool,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[List[BaseAction]]:
        choices: List[Dict[str, Any]] = [
            {"name": f"{action} (level {level})",
             "value": action}
            for (action, level) in possible_expedition_rewards
        ]

        def expedition_reward_validator(rewards: List[BaseAction]) -> bool:
            return len(rewards) <= expedition_level

        def transform(_) -> str:
            text = []
            non_receive_rewards: List[BaseAction] = []
            receive_rewards: List[ReceiveAction] = []

            for reward in chosen_rewards_prompt.result_value:
                if isinstance(reward, ReceiveAction):
                    receive_rewards.append(reward)
                    continue
                non_receive_rewards.append(reward)

            if len(receive_rewards) > 0:
                text.append("Receive ")
                for (i, reward) in enumerate(receive_rewards):
                    for (j, (item, amount)) in enumerate(reward._items_to_receive.items()):
                        text.append(f"{amount} {item.name}")
                        if j != len(reward._items_to_receive) - 1:
                            text.append(" and ")
                    if i != len(receive_rewards) - 1:
                        text.append(" and ")
                if len(non_receive_rewards) > 0:
                    text.append(", and then ")

            for (i, reward) in enumerate(non_receive_rewards):
                text.append(str(reward))
                if i != len(non_receive_rewards) - 1:
                    text.append(" and ")

            return "".join(text)

        chosen_rewards_prompt = inquirer.checkbox(
            message="Pick an expedition reward",
            choices=choices,
            validate=expedition_reward_validator,
            instruction="Use ↑/↓ to pick the rewards, and press space to select",
            invalid_message="should be only one reward" if expedition_level == 1 else f"should be at most {expedition_level} selected",
            transformer=transform
        )

        self._add_keybinding_that_shows_resources(chosen_rewards_prompt)

        chosen_rewards: List[BaseAction] = chosen_rewards_prompt.execute()

        result: ResultLookup[List[BaseAction]] = ResultLookup(True, chosen_rewards)
        return result

    def get_player_choice_location_to_build(
            self,
            tile: BaseTile,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[int]:
        if tile is None:
            raise ValueError("Tile cannot be None")

        location_name: str = "location_to_use"

        from common.services.tile_service import TileService
        tile_service: TileService = TileService()

        valid_locations: ValidLocations
        location: Optional[int] = None
        options = TilePlacementOptions()

        while location is None:
            if options.needs_clean:
                valid_locations = tile_service.get_available_locations_for_single(self, tile.tile_type)
                options.needs_clean = False
                if options.ignore_adjacency:
                    valid_locations.ignore_adjacency()
                if options.ignore_requisites:
                    valid_locations.ignore_requisites()
            location = self._create_prompt_for_tile_placement(valid_locations, options).execute()

        result: ResultLookup[int] = ResultLookup(True, location)

        return result

    def get_player_choice_location_to_build_twin(
            self,
            tile_type: TileTypeEnum,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[TileTwinPlacementLookup]:
        from common.services.tile_service import TileService
        tile_service: TileService = TileService()

        valid_locations: ValidTwinTileLocations
        location: Optional[int] = None
        options = TilePlacementOptions()

        while location is None:
            if options.needs_clean:
                valid_locations: ValidTwinTileLocations = tile_service.get_available_locations_for_twin(self, tile_type)
                options.needs_clean = False
                if options.ignore_adjacency:
                    valid_locations.ignore_adjacency()
                if options.ignore_requisites:
                    valid_locations.ignore_requisites()
            location = self._create_prompt_for_tile_placement(valid_locations, options).execute()

        placement = inquirer.select(
            message="Pick a direction",
            choices=[
                {"name": placement.name,
                 "value": placement}
                for placement in
                valid_locations[location]
            ]).execute()

        result: ResultLookup[TileTwinPlacementLookup] = ResultLookup(True, TileTwinPlacementLookup(location, placement))

        return result

    def get_player_choice_location_to_build_stable(
            self,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[int]:
        from common.services.tile_service import TileService
        tile_service: TileService = TileService()

        valid_locations: List[int]
        location: Optional[int] = None
        options = TilePlacementOptions()

        while location is None:
            if options.needs_clean:
                valid_locations = tile_service.get_available_locations_for_stable(self)
                options.needs_clean = False
                if options.ignore_adjacency:
                    valid_locations.ignore_adjacency()
                if options.ignore_requisites:
                    valid_locations.ignore_requisites()
            location = self._create_prompt_for_tile_placement(valid_locations, options).execute()

        return ResultLookup(True, location)

    def get_player_choice_effects_to_use_for_cost_discount(
            self,
            tile_cost: Dict[ResourceTypeEnum, int],
            possible_effects: List[BaseTilePurchaseEffect],
            turn_descriptor: TurnDescriptorLookup) -> Dict[BaseTilePurchaseEffect, int]:
        possible_effects: List[Dict[str, BaseTilePurchaseEffect]] = []

        use_effects = True
        has_ever_shown_cost = False

        while use_effects:
            use_effects_prompt = inquirer.confirm(
                message="Use effects to reduce cost?",
                default=False,
                instruction="(y/N)" if has_ever_shown_cost else "(y/N/c)",
                mandatory=has_ever_shown_cost)

            use_effects_prompt.has_shown_cost = has_ever_shown_cost

            @use_effects_prompt.register_kb("c")
            def _handle_cost(event):
                if use_effects_prompt.has_shown_cost:
                    return
                use_effects_prompt.has_shown_cost = True
                text = [("", "  Tile costs: ")]

                append_resources(text, tile_cost, lambda text: text.append(("", "nothing")))
                color_print(text, style={"count": "yellow"})
                use_effects_prompt._handle_skip(event)

            use_effects = use_effects_prompt.execute()

            has_ever_shown_cost |= use_effects_prompt.has_shown_cost

            if use_effects is None:
                use_effects = True
                continue

            if use_effects:
                effects_to_use = inquirer.checkbox(
                    message="Pick effects to use",
                    choices=[],
                    mandatory=False
                ).execute()

                if effects_to_use is not None:
                    return {effect: 1 for effect in effects_to_use}
        return {}

    def get_player_choice_use_harvest_action_instead_of_breeding(
            self,
            turn_descriptor: TurnDescriptorLookup) -> bool:
        return True

    def get_player_choice_effect_to_use_for_feeding_dwarves(
            self,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[List[BaseFoodEffect]]:
        return ResultLookup(True, [])

    def get_player_choice_resources_to_sow(
            self,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ResourcesToSow]:
        grain_to_sow_prompt = inquirer.number(
            message="How many grain do you wish to sow",
            min_allowed=0,
            max_allowed=2)

        self._add_keybinding_that_shows_resources(grain_to_sow_prompt)
        self._add_keybinding_that_shows_round_info(grain_to_sow_prompt, turn_descriptor)

        grain_to_sow = int(grain_to_sow_prompt.execute())

        veg_to_sow_prompt = inquirer.number(
            message="How many veg do you wish to sow",
            min_allowed=0,
            max_allowed=2)

        self._add_keybinding_that_shows_resources(veg_to_sow_prompt)
        self._add_keybinding_that_shows_round_info(veg_to_sow_prompt, turn_descriptor)

        veg_to_sow = int(veg_to_sow_prompt.execute())

        result: ResultLookup[ResourcesToSow] = ResultLookup(True, ResourcesToSow(grain_to_sow, veg_to_sow))
        return result

    def _add_keybinding_that_shows_resources(
            self,
            prompt: 'InquirerPy.base.simple.BaseSimplePrompt') -> None:
        prompt.has_shown_resources = False

        @prompt.register_kb("r")
        def _handle_resources(event):
            if prompt.has_shown_resources:
                return
            prompt.has_shown_resources = True

            text = [
                ("class:pointer", "❯ "),
                ("", "resources available to player ("),
                ("class:player", self.descriptor),
                ("", ") at start of turn: ")
            ]
            append_resources(text, self.resources, lambda text: text.append(("", "none")))
            color_print(text, style={
                "pointer": "#e5c07b",
                "count": "#61afef",
                "player": "ansimagenta"})

    def _add_keybinding_that_shows_round_info(
            self,
            prompt: 'InquirerPy.base.simple.BaseSimplePrompt',
            turn_descriptor: TurnDescriptorLookup) -> None:
        prompt.has_shown_round_info = False

        @prompt.register_kb("q")
        def _handle_resources(event):
            if prompt.has_shown_round_info:
                return
            prompt.has_shown_round_info = True

            text = [
                ("class:pointer", "❯ "),
                ("", "round"),
                ("class:round", str(turn_descriptor.round_index + 1)),
                ("", " "),
                ("class:player", self.descriptor),
            ]
            append_resources(text, self.resources, lambda text: text.append(("", "none")))
            color_print(text, style={
                "pointer": "#98c379",
                "count": "#61afef",
                "player": "ansimagenta"})

    def _create_map_for_tile_placement(self, valid_locations) -> Printable:
        # _ 1 2 _ | _ _ _ 7
        # 8 x x x | x x x _
        # _ x x x | x _ x _
        # _ x x27 | C _ x _
        # _ x x x | D x x _
        # _ _ _ _ | _ _ _ _

        index: int = 0
        tiles_map: List[Tuple[List[str], List[str]]] = []

        for y in range(self.height):
            line_map_readable: List[str] = []
            line_map_number: List[str] = []
            for x in range(self.width):
                tile_type_at_index: TileTypeEnum = self.tiles[index].tile_type
                if (index % self.width) == math.floor(self.width / 2):
                    line_map_readable.append("|")
                    line_map_number.append("|")
                is_tile_type_unavailable: bool = tile_type_at_index is TileTypeEnum.unavailable
                is_location_valid: bool = index in valid_locations

                tile_value_readable: str
                tile_value_number: str

                if is_location_valid:
                    if not (tile_type_at_index is TileTypeEnum.furnishedDwelling
                            or tile_type_at_index is TileTypeEnum.furnishedCavern):
                        tile_value_readable = tile_type_at_index.name[0:2]
    #                        tile_value_readable = tile_type_at_index.name[:2].rjust(2)
                    else:
                        tile_value_readable = self.tiles[index].tile.name[:2]
                    tile_value_number = str(index).rjust(2)
                elif not is_tile_type_unavailable:
                    tile_value_readable = " _"
                    tile_value_number = " _"
                else:
                    tile_value_readable = "  "
                    tile_value_number = "  "

                line_map_readable.append(tile_value_readable)
                line_map_number.append(tile_value_number)

                index += 1
            tiles_map.append((line_map_readable, line_map_number))

        result = ""
        for line_map_readable in tiles_map:
            result += f"{' '.join(line_map_readable[0])}    {' '.join(line_map_readable[1])}\r\n"
        return result

    def _create_prompt_for_tile_placement(
            self,
            valid_locations,
            prompt_options: TilePlacementOptions):
        from prompt_toolkit.validation import Validator

        additional_information = self._create_map_for_tile_placement(valid_locations)
        if isinstance(additional_information, str):
            print(additional_information)
        else:
            color_print(additional_information[0], additional_information[1])

        def format_result(result: str | None):
            if result is not None:
                return result
            if prompt_options.ignore_requisites:
                if prompt_options.ignore_adjacency:
                    return "allow tile to be placed anywhere"
                return "allow tile to be placed on any type"
            if prompt_options.ignore_adjacency:
                return "allow tile to be placed on unconnected tiles"
            return "allow tile to be placed on locations that were valid at start of turn"

        default_message = "Choose a location"

        prompt = inquirer.number(
            message=default_message,
            min_allowed=valid_locations.minimum(),
            max_allowed=valid_locations.maximum(),
            filter=lambda result: None if result is None else int(result),
            instruction="Use ↑/↓ to pick the location",
            mandatory=False
        )

        def validate_location(chosen_location: str) -> bool:
            location_is_valid: bool = chosen_location.isdigit()
            if location_is_valid:
                location_is_valid = int(chosen_location) in valid_locations
            return location_is_valid

        prompt.validator = Validator.from_callable(validate_location)

        def _handle_next_location(event):
            #patched_print("spin up")
            #patched_print(f" {event=}")
            #patched_print(f" {prompt._whole_buffer=}")
            #patched_print(f" {prompt._integral_buffer=}")
            current_location = int(prompt._whole_buffer.text)

            has_current_location_been_found = False
            for location in valid_locations:
                if location == current_location:
                    has_current_location_been_found = True
                    continue
                if has_current_location_been_found:
                    prompt._whole_buffer.text = str(location)
                    return
            prompt._whole_buffer.text = str(valid_locations.maximum())

        def _handle_previous_location(event):
            #patched_print("spin down")
            #patched_print(f" {event=}")
            #patched_print(f" {prompt._whole_buffer=}")
            #patched_print(f" {prompt._integral_buffer=}")
            current_location = int(prompt._whole_buffer.text)
            has_current_location_been_found = False
            for location in reversed(valid_locations):
                if location == current_location:
                    has_current_location_been_found = True
                    continue
                if has_current_location_been_found:
                    prompt._whole_buffer.text = str(location)
                    return
            prompt._whole_buffer.text = str(valid_locations.minimum())

        prompt.kb_func_lookup["up"][0]["func"] = _handle_next_location
        prompt.kb_func_lookup["down"][0]["func"] = _handle_previous_location
        del prompt.kb_func_lookup["input"][0]

        @prompt.register_kb("r")
        def _handle_change_tile_validity(event):
            if prompt_options.ignore_requisites:
                prompt_options.ignore_requisites = False
                prompt_options.needs_clean = True
                prompt._message = "Changing valid locations to " + format_result(None)
                prompt._handle_skip(event)
                return
            prompt_options.ignore_requisites = True
            valid_locations.ignore_requisites()
            prompt._message = "Changing valid locations to " + format_result(None)
            prompt._handle_skip(event)

        @prompt.register_kb("a")
        def _handle_change_tile_validity(event):
            if prompt_options.ignore_adjacency:
                prompt_options.ignore_adjacency = False
                prompt_options.needs_clean = True
                prompt._message = "Changing valid locations to " + format_result(None)
                prompt._handle_skip(event)
                return
            prompt_options.ignore_adjacency = True
            valid_locations.ignore_adjacency()
            prompt._message = "Changing valid locations to " + format_result(None)
            prompt._handle_skip(event)

        return prompt
