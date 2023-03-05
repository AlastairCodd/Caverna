import math
from enum import Enum
from typing import List, Tuple, Optional, Dict, Any, Union, Callable

#from InquirerPy.utils import patched_print
from InquirerPy.utils import color_print
from InquirerPy import inquirer, prompt

from buisness_logic.effects.food_effects import BaseFoodEffect
from buisness_logic.effects.purchase_effects import BaseTilePurchaseEffect
from common.defaults.tile_container_default import TileContainerDefault
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.tile_twin_placement_lookup import TileTwinPlacementLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_tile import BaseTile
from core.containers.resource_container import ResourceContainer
from core.enums.caverna_enums import ResourceTypeEnum, TileTypeEnum
from core.services.base_player_service import BasePlayerService


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
        text.append(("class:amount", str(amount)))
        text.append(("", " "))
        text.append(("class:resource", resource.name))
        if i < len(resources) - 1:
            text.append(("", ", "))


class QuestionTypeEnum(Enum):
    confirm = 0,
    list = 1,
    input = 2,
    checkbox = 3,


def create_question(
        question_type: QuestionTypeEnum,
        name: str,
        message: str,
        choices: Optional[Union[List[Union[str, Dict[str, Any]]], Callable[[Dict[str, Any]], List[Dict[str, Any]]]]] = None,
        validator: Optional[Callable[[Any], bool]] = None,
        default: Optional[Any] = None,
        when: Optional[Callable[[Dict[str, Any]], bool]] = None) -> Dict[str, Any]:
    type_name: str = {
        QuestionTypeEnum.confirm: "confirm",
        QuestionTypeEnum.list: "list",
        QuestionTypeEnum.input: "input",
        QuestionTypeEnum.checkbox: "checkbox",
    }[question_type]

    result: Dict[str, Any] = {
        "type": type_name,
        "message": message,
        "name": name,
    }

    if choices is not None:
        result["choices"] = choices
    if validator is not None:
        result["validate"] = validator
    if default is not None:
        result["default"] = default
    if when is not None:
        result["when"] = when

    return result


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

    def get_player_choice_conversions_to_perform(
            self,
            turn_descriptor: TurnDescriptorLookup) -> List[Tuple[List[ResourceTypeEnum], int, List[ResourceTypeEnum]]]:
        pass

    def get_player_choice_market_items_to_purchase(
            self,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[List[ResourceTypeEnum]]:
        raise NotImplementedError()

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
        pass

    def get_player_choice_use_dwarf_out_of_order(
            self,
            dwarves: List[Dwarf],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[bool]:
        if dwarves is None:
            raise ValueError("Dwarves may not be None")
        name = "use_dwarf_out_of_order"
        question: Dict[str, Any] = create_question(
            QuestionTypeEnum.confirm,
            "Use Dwarf out of Order?",
            name,
            default=False
        )

        answer = prompt(question)
        result: ResultLookup[bool] = ResultLookup(answer[name], answer[name])
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

            card_description: List[str] = [f"Confirm that you'd like to use {card_to_use.name}?"]
            if card_to_use.actions is not None:
                card_description.append("  Actions: ")
                card_description.append(f"    {card_to_use.actions:4}")
            if isinstance(card_to_use, ResourceContainer) and card_to_use.has_resources:
                card_description.append("  Resources: ")
                card_description.extend([f"    {resource.name}: {amount}" for resource, amount in card_to_use.resources.items()])
            confirm_message: str = "\n".join(card_description)
            print(confirm_message)

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

        name = "card_to_use"
        question: Dict[str, Any] = create_question(
            QuestionTypeEnum.list,
            name,
            "Pick a Dwarf",
            choices=choices
        )

        answer = prompt(question)
        result: ResultLookup[Dwarf] = ResultLookup(True, answer[name])
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

        name = "actions_to_use"
        question: Dict[str, Any] = create_question(
            QuestionTypeEnum.list,
            name,
            "Choose some actions to use",
            choices=choices
        )

        answer = prompt(question)
        result: ResultLookup[ActionChoiceLookup] = ResultLookup(True, answer[name])
        return result

    def get_player_choice_tile_to_build(
            self,
            possible_tiles: List[BaseTile],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[BaseTile]:
        if possible_tiles is None:
            raise ValueError("Possible Tiles cannot be None")
        if len(possible_tiles) == 0:
            raise ValueError("Possible Tiles cannot be empty")

        prompt = inquirer.select(
            message="Pick a tile to build",
            choices=[
                {"name": tile.name,
                 "value": tile}
                for tile in possible_tiles
            ],
            long_instruction="Navigate with arrow keys, press c to see the cost of the currently selected tile"
        )

        prompt.last_card_to_show_cost = None

        @prompt.register_kb("c")
        def _handle_cost(event):
            if prompt.last_card_to_show_cost == prompt.result_value:
                return
            prompt.last_card_to_show_cost = prompt.result_value
            text = [("", "  "), ("", prompt.result_value.name), ("", " costs: ")]

            append_resources(text, prompt.result_value.cost, lambda text: text.append(("", "nothing")))
            color_print(text, style={"amount": "yellow"})

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

        chosen_rewards_prompt = inquirer.checkbox(
             message="Pick an expedition reward",
             choices=choices,
             validate=expedition_reward_validator,
             invalid_message="should be only one reward" if expedition_level == 1 else f"should be at most {expedition_level} selected"
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

        valid_locations: List[int] = tile_service.get_available_locations_for_single(self, tile.tile_type)

        additional_information = self._create_map_for_tile_placement(valid_locations)
        if isinstance(additional_information, str):
            print(additional_information)
        else:
            color_print(additional_information[0], additional_information[1])

        location = self._create_prompt_for_tile_placement(valid_locations).execute()

        result: ResultLookup[int] = ResultLookup(True, int(location))

        return result

    def get_player_choice_location_to_build_twin(
            self,
            tile_type: TileTypeEnum,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[TileTwinPlacementLookup]:
        from common.services.tile_service import TileService
        tile_service: TileService = TileService()

        locations_for_twin: List[TileTwinPlacementLookup] = tile_service.get_available_locations_for_twin(self, tile_type)
        valid_locations: Dict[int, List[TileTwinPlacementLookup]] = {}
        for tile_placement in locations_for_twin:
            location: int = tile_placement.location
            if location in valid_locations:
                valid_locations[location].append(tile_placement)
            else:
                valid_locations[location] = [tile_placement]

        additional_information = self._create_map_for_tile_placement(valid_locations)
        if isinstance(additional_information, str):
            print(additional_information)
        else:
            color_print(additional_information[0], additional_information[1])

        prompt = self._create_prompt_for_tile_placement(valid_locations)

        location = prompt.execute()

        if location is None:
            return ResultLookup("Choosing location cancelled")

        placement = inquirer.select(
            message="Pick a direction",
            choices=[
                {"name": placement.direction.name,
                 "value": placement}
                for placement in
                valid_locations[int(location)]
            ]).execute()

        result: ResultLookup[TileTwinPlacementLookup] = ResultLookup(True, placement)

        return result

    def get_player_choice_location_to_build_stable(
            self,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[int]:
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

                tile_value_readable: str
                tile_value_number: str

                if not is_tile_type_unavailable:
                    if not (tile_type_at_index is TileTypeEnum.furnishedDwelling
                            or tile_type_at_index is TileTypeEnum.furnishedCavern):
                        tile_value_readable = tile_type_at_index.name[0].rjust(2)
                    else:
                        tile_value_readable = self.tiles[index].tile.name[:2]
                    tile_value_number = str(index).rjust(2)
                else:
                    tile_value_readable = "  "
                    tile_value_number = "  "

                line_map_readable.append(tile_value_readable)
                line_map_number.append(tile_value_number)

                index += 1
            tiles_map.append((line_map_readable, line_map_number))

        for line_map_readable in tiles_map:
            print(" ".join(line_map_readable[0]), end="    ")
            print(" ".join(line_map_readable[1]))

        location_name: str = "location_to_use"

        def validate_location(chosen_location: str) -> bool:
            location_is_valid: bool = chosen_location.isspace() or chosen_location == "" or chosen_location.isdigit()
            if chosen_location.isdigit():
                location_is_valid = 0 <= int(chosen_location) < self.tile_count
            return location_is_valid

        questions: List[Dict[str, Any]] = [
            create_question(
                QuestionTypeEnum.input,
                location_name,
                "Choose a location",
                validator=validate_location
            )
        ]

        answers: Dict[str, Any] = prompt(questions)

        location_to_build = answers[location_name]
        result: ResultLookup[int]

        if location_to_build.isdigit():
            result = ResultLookup(True, int(location_to_build))
        else:
            result = ResultLookup(errors="Dialog Cancelled")

        return result

    def get_player_choice_effects_to_use_for_cost_discount(
            self,
            tile_cost: Dict[ResourceTypeEnum, int],
            possible_effects: List[BaseTilePurchaseEffect],
            turn_descriptor: TurnDescriptorLookup) -> Dict[BaseTilePurchaseEffect, int]:
        use_any_effects_name: str = "use_any_effects_name"
        effects_to_use_name: str = "effects_to_use_name"

        possible_effects: List[Dict[str, BaseTilePurchaseEffect]] = []

        questions: List[Dict[str, Any]] = [
            create_question(
                QuestionTypeEnum.confirm,
                use_any_effects_name,
                f"Use effects to reduce tile cost?\nCost: {tile_cost}"
            ),
            create_question(
                QuestionTypeEnum.checkbox,
                effects_to_use_name,
                "Pick effects to use",
                choices=possible_effects,
                when=lambda current_answers: current_answers[use_any_effects_name]
            ),
            ]

        answers: Dict[str, Any] = prompt(questions)

        result: Dict[BaseTilePurchaseEffect, int] = {}
        if answers[use_any_effects_name]:
            raise NotImplementedError()
        return result

    def get_player_choice_use_harvest_action_instead_of_breeding(
            self,
            turn_descriptor: TurnDescriptorLookup) -> bool:
        pass

    def get_player_choice_effect_to_use_for_feeding_dwarves(
            self,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[List[BaseFoodEffect]]:
        pass

    def get_player_choice_resources_to_sow(
            self,
            number_of_resources_to_sow: int,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[List[ResourceTypeEnum]]:
        print("Resources at start of turn")
        print(f"Grain: {self.get_resources_of_type(ResourceTypeEnum.grain)}")
        print(f"Veg: {self.get_resources_of_type(ResourceTypeEnum.veg)}")

        resources_to_use: List[ResourceTypeEnum] = []

        resource_name: str = "resource_to_use"
        choices: List[Dict[str, Any]] = [
            {"name": choice.name,
             "value": choice, }
            for choice in [ResourceTypeEnum.grain, ResourceTypeEnum.veg]]

        questions = [
            create_question(
                QuestionTypeEnum.list,
                resource_name,
                "Choose resource to build",
                choices=choices)
        ]

        for _ in range(number_of_resources_to_sow):
            answers: Dict[str, Any] = prompt(questions)
            resources_to_use.append(answers[resource_name])

        result: ResultLookup[List[ResourceTypeEnum]] = ResultLookup(True, resources_to_use)
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
                "amount": "#61afef",
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

    def _create_prompt_for_tile_placement(self, valid_locations):
        def validate_location(chosen_location: str) -> bool:
            location_is_valid: bool = chosen_location.isdigit()
            if location_is_valid:
                location_is_valid = int(chosen_location) in valid_locations
            return location_is_valid

        prompt = inquirer.number(
            message="Choose a location",
            min_allowed=min(valid_locations),
            max_allowed=max(valid_locations),
            validate=validate_location,
            instruction="Use ↑/↓ to pick the location"
        )

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
            prompt._whole_buffer.text = str(max(valid_locations))

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
            prompt._whole_buffer.text = str(min(valid_locations))

        prompt.kb_func_lookup["up"][0]["func"] = _handle_next_location
        prompt.kb_func_lookup["down"][0]["func"] = _handle_previous_location
        del prompt.kb_func_lookup["input"][0]

        return prompt
