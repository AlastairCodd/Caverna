import math
from enum import Enum
from typing import List, Tuple, Optional, Dict, Any, Union, Callable

from PyInquirer import prompt

from buisness_logic.effects.food_effects import BaseFoodEffect
from buisness_logic.effects.purchase_effects import BaseTilePurchaseEffect
from common.defaults.tile_container_default import TileContainerDefault
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.tile_twin_placement_lookup import TileTwinPlacementLookup
from common.entities.tile_unknown_placement_lookup import TileUnknownPlacementLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_tile import BaseTile
from core.containers.resource_container import ResourceContainer
from core.enums.caverna_enums import ResourceTypeEnum, TileTypeEnum
from core.services.base_player_service import BasePlayerService


class QuestionTypeEnum(Enum):
    confirm = 0,
    list = 1,
    input = 2,


def create_question(
        question_type: QuestionTypeEnum,
        name: str,
        message: str,
        choices: Optional[Union[List[Union[str, Dict[str, Any]]], Callable[[Dict[str, Any]], List[Dict[str, Any]]]]] = None,
        validator: Optional[Callable[[Any], bool]] = None,
        default: Optional[Any] = None) -> Dict[str, Any]:
    type_name: str = {
        QuestionTypeEnum.confirm: "confirm",
        QuestionTypeEnum.list: "list",
        QuestionTypeEnum.input: "input",
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

    return result


class KeyboardHumanPlayerService(BasePlayerService):
    def __init__(
            self,
            player_id: int,
            player_turn_index: int) -> None:
        BasePlayerService.__init__(
            self,
            player_id,
            player_turn_index,
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
        name = "use_card_already_in_use"
        question: Dict[str, Any] = create_question(
            QuestionTypeEnum.confirm,
            "Use card already in use?",
            name,
            default=False
        )

        answer = prompt(question)
        result: bool = answer[name]
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

        card_to_use_name: str = "card_to_use"
        confirm_use_name: str = "confirm_card"

        has_picked_card: bool = False
        card_answer: Dict[str, Any] = {}

        while not has_picked_card:
            card_question: Dict[str, Any] = create_question(
                QuestionTypeEnum.list,
                card_to_use_name,
                "Pick a card",
                choices=choices
            )

            card_answer = prompt(card_question)

            card_to_use: BaseCard = card_answer[card_to_use_name]

            card_description: List[str] = [f"Confirm using {card_to_use.name}?"]
            if card_to_use.actions is not None:
                card_description.append("  Actions: ")
                card_description.append(f"    {str(card_to_use.actions)}")
            if isinstance(card_to_use, ResourceContainer) and card_to_use.has_resources:
                card_description.append("  Resources: ")
                card_description.extend([f"    {resource.name}: {amount}" for resource, amount in card_to_use.resources.items()])
            confirm_message: str = "\n".join(card_description)
            print(confirm_message)

            confirm_question: Dict[str, Any] = create_question(
                QuestionTypeEnum.confirm,
                confirm_use_name,
                ""
            )

            confirm_answer: Dict[str, Any] = prompt(confirm_question)

            has_picked_card = confirm_answer[confirm_use_name]

        result: ResultLookup[BaseCard] = ResultLookup(True, card_answer[card_to_use_name])
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

        choices: List[Dict[str, Any]] = [
            {"name": tile.name,
             "value": tile}
            for tile in possible_tiles]

        tile_to_build_name: str = "tile_to_build"
        questions: List[Dict[str, Any]] = [
            create_question(
                QuestionTypeEnum.list,
                tile_to_build_name,
                "Pick a tile to build",
                choices=choices
            )
        ]
        answers: Dict[str, Any] = prompt(questions)
        result: ResultLookup[BaseTile] = ResultLookup(True, answers[tile_to_build_name])
        return result

    def get_player_choice_expedition_reward(
            self,
            possible_expedition_rewards: List[BaseAction],
            expedition_level: int,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[List[BaseAction]]:
        choices: List[Dict[str, Any]] = [
            {"name": str(action),
             "value": action}
            for action in possible_expedition_rewards
        ]

        expedition_reward_name: str = "expedition_reward_name"
        chosen_rewards: List[BaseAction] = []

        def expedition_reward_validator(reward: BaseAction) -> bool:
            is_valid: bool = reward not in chosen_rewards
            return is_valid

        questions: List[Dict[str, Any]] = [
            create_question(
                QuestionTypeEnum.list,
                expedition_reward_name,
                "Pick an expedition reward",
                choices=choices,
                validator=expedition_reward_validator
            )
        ]

        for _ in range(expedition_level):
            answers: Dict[str, Any] = prompt(questions)
            chosen_reward: BaseAction = answers[expedition_reward_name]
            chosen_rewards.append(chosen_reward)

        result: ResultLookup[List[BaseAction]] = ResultLookup(True, chosen_rewards)
        return result

    def get_player_choice_location_to_build(
            self,
            tile: BaseTile,
            turn_descriptor: TurnDescriptorLookup,
            secondary_tile: Optional[BaseTile] = None) -> ResultLookup[TileUnknownPlacementLookup]:
        if tile is None:
            raise ValueError("Tile cannot be None")

        location_name: str = "location_to_use"
        direction_name: str = "direction_to_point"

        from common.services.tile_service import TileService
        tile_service: TileService = TileService()

        valid_locations: Union[List[int], Dict[int, List[TileTwinPlacementLookup]]]
        is_outdoors_tile: bool = tile_service.is_tile_placed_outside(tile.tile_type)
        requisites: List[TileTypeEnum] = tile_service.outdoor_tiles \
            if is_outdoors_tile \
            else [tile for tile in TileTypeEnum if tile not in tile_service.outdoor_tiles]

        if secondary_tile is None:
            valid_locations = tile_service.get_available_locations_for_single(self, tile.tile_type, requisites)
        else:
            locations_for_twin: List[TileTwinPlacementLookup] = tile_service.get_available_locations_for_twin(self, requisites_override=requisites)
            valid_locations_for_twin: Dict[int, List[TileTwinPlacementLookup]] = {}
            for tile_placement in locations_for_twin:
                location: int = tile_placement.location
                if location in valid_locations_for_twin:
                    valid_locations_for_twin[location].append(tile_placement)
                else:
                    valid_locations_for_twin[location] = [tile_placement]
            valid_locations = valid_locations_for_twin

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
                        tile_value_readable = tile_type_at_index.name[0].rjust(2)
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

        for line_map_readable in tiles_map:
            print(" ".join(line_map_readable[0]), end="    ")
            print(" ".join(line_map_readable[1]))

        def validate_location(chosen_location: str) -> bool:
            location_is_valid: bool = not (chosen_location.isspace() or chosen_location == "")
            if location_is_valid:
                location_is_valid = int(chosen_location) in valid_locations
            return location_is_valid

        questions: List[Dict[str, Any]] = [create_question(
            QuestionTypeEnum.input,
            location_name,
            "Choose a location",
            validator=validate_location
        )]

        if secondary_tile is not None:
            def direction_choices(current_answers: Dict[str, Any]) -> List[Dict[str, Any]]:
                return [
                    {"name": placement.direction.name,
                     "value": placement}
                    for placement in
                    valid_locations[int(current_answers[location_name])]]

            direction_question: Dict[str, Any] = create_question(
                QuestionTypeEnum.list,
                direction_name,
                "Pick a direction",
                choices=direction_choices
            )
            questions.append(direction_question)

        answers = prompt(questions)

        result: ResultLookup[TileUnknownPlacementLookup]
        if secondary_tile is None:
            result = ResultLookup(True, TileUnknownPlacementLookup(answers[location_name], None))
        else:
            result = ResultLookup(True, answers[direction_name])

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

        questions = [
            create_question(
                QuestionTypeEnum.input,
                location_name,
                "Choose a location",
                validator=validate_location
            )
        ]

        locations_to_build: List[int] = []

        for _ in range(number_of_resources_to_sow):
            answers: Dict[str, Any] = prompt(questions)
            location_to_build = answers[location_name]
            if location_to_build.isdigit():
                locations_to_build.append(int(location_to_build))

        result: ResultLookup[List[int]] = ResultLookup(True, locations_to_build)
        return result

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
