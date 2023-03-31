import math
from collections import Counter
from typing import Dict, List

from buisness_logic.effects.conversion_effects import ConvertEffect
from buisness_logic.effects.resource_effects import ReceiveOnConvertFromEffect
from buisness_logic.services.base_receive_event_service import BaseReceiveEventService
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.containers.tile_container import TileContainer
from core.enums.caverna_enums import ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository


class ConvertSingleAction(BaseAction, BaseReceiveEventService):
    def __init__(
            self,
            convert_from: List[ResourceTypeEnum],
            convert_to: List[ResourceTypeEnum],
            number_of_times: int) -> None:
        if convert_from is None or len(convert_from) == 0:
            raise ValueError("Must Convert From some resource")
        if convert_to is None or len(convert_to) == 0:
            raise ValueError("Must Convert To some resource")
        if number_of_times <= 0:
            raise ValueError("Cannot convert a negative number of times")
        self._convert_from: List[ResourceTypeEnum] = convert_from
        self._convert_to: List[ResourceTypeEnum] = convert_to
        self._number_of_times: int = number_of_times

    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        if player is None:
            raise ValueError("Player cannot be None")

        result: ResultLookup[int]

        required_conversion_effects: Dict[int, ConvertEffect] = self._get_required_conversion_effects(player)
        if len(required_conversion_effects) == 0:
            return ResultLookup(errors=f"Player does not have effect allowing conversion from {self._convert_from} to {self._convert_from}")

        errors: List[str] = []

        conversions_to_use: Dict[ConvertEffect, int] = self._get_conversion_effect_to_use(required_conversion_effects)

        resources_to_take: Dict[ResourceTypeEnum, int] = {}
        resources_to_give: Dict[ResourceTypeEnum, int] = {}
        for effect, number_of_times_to_use in conversions_to_use.items():
            for resource in effect.input:
                resources_to_take[resource] = effect.input[resource] * number_of_times_to_use + resources_to_take.get(resource, 0)
            for resource in effect.output:
                resources_to_give[resource] = effect.output[resource] * number_of_times_to_use + resources_to_give.get(resource, 0)

        receive_on_convert_from_effects: List[ReceiveOnConvertFromEffect] = player.get_effects_of_type(ReceiveOnConvertFromEffect)

        for effect in receive_on_convert_from_effects:
            if effect.convert_from_item not in resources_to_take:
                continue
            number_of_times_taken: int = resources_to_take[effect.convert_from_item]
            for resource in effect.items_to_receive:
                resources_to_give[resource] = effect.items_to_receive[resource] * number_of_times_taken + resources_to_give.get(resource, 0)

        does_player_have_more_resources_than_taken: bool = player.has_more_resources_than(resources_to_take)
        if not does_player_have_more_resources_than_taken:
            errors.append("Player does not have sufficient resources to convert from")

        if len(errors) > 0:
            return ResultLookup(errors=errors)

        if not player.take_resources(resources_to_take):
            return ResultLookup(errors="DEV ERROR: Taking resources failed.")

        result = self._give_player_resources(player, resources_to_give)
        return result

    def new_turn_reset(self) -> None:
        pass

    def _get_required_conversion_effects(
            self,
            player: TileContainer) -> Dict[int, ConvertEffect]:
        if player is None:
            raise ValueError("Player cannot be None")
        convert_effects: List[ConvertEffect] = player.get_effects_of_type(ConvertEffect)

        required_conversion_effects: Dict[int, ConvertEffect] = {}

        for effect in convert_effects:
            # CONFIG: consider using this if can convert none of some resource can be lost
            are_converting_from_same: bool = all(resource in self._convert_from for resource in effect.input)
            # are_converting_from_same: bool = Counter(effect.input.keys()) == Counter(self._convert_from)
            if not are_converting_from_same:
                continue
            # CONFIG: consider using this if gaining non-asked for resources is desired
            # are_converting_to_same: bool = all(resource in effect.output for resource in self._convert_to)
            are_converting_to_same: bool = Counter(effect.output.keys()) == Counter(self._convert_to)
            if not are_converting_to_same:
                continue
            number_of_times_input_is_converted_in_effect: int = min(effect.input.values())
            required_conversion_effects[number_of_times_input_is_converted_in_effect] = effect

        return required_conversion_effects

    def _get_conversion_effect_to_use(
            self,
            conversion_effects: Dict[int, ConvertEffect]) -> Dict[ConvertEffect, int]:
        if conversion_effects is None:
            raise ValueError("Conversion effects cannot be null")
        number_of_conversion_effects: int = len(conversion_effects)
        if number_of_conversion_effects == 0:
            raise ValueError("Must have at least one conversion effect")

        if number_of_conversion_effects == 1:
            effect_to_use: ConvertEffect
            number_of_times_input_is_converted_in_effect, effect_to_use = next(iter(conversion_effects.items()))

            number_of_times_to_use_effect: int = math.floor(self._number_of_times / number_of_times_input_is_converted_in_effect)
            return {effect_to_use: number_of_times_to_use_effect}

        remaining_times: int = self._number_of_times
        current_index: int = self._number_of_times

        result: Dict[ConvertEffect, int] = {}

        while remaining_times > 0:
            if current_index in conversion_effects:
                number_of_times_to_use_conversion_effect: int = math.floor(remaining_times / current_index)
                result[conversion_effects[current_index]] = number_of_times_to_use_conversion_effect
                remaining_times -= number_of_times_to_use_conversion_effect * current_index

            current_index -= 1

        return result

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False

        are_converting_from_same: bool = Counter(other._convert_from) == Counter(self._convert_from)
        are_converting_to_same: bool = Counter(other._convert_to) == Counter(self._convert_to)
        are_converting_same_number_of_times: bool = other._number_of_times == self._number_of_times

        result: bool = are_converting_to_same and are_converting_from_same and are_converting_same_number_of_times
        return result

    def __str__(self) -> str:
        return self.__format__(" ")

    def __format__(self, format_spec):
        text = [("", "Convert ")]
        for (i, resource) in enumerate(self._convert_from):
            text.append(("class:resource", resource.name))
            if i == len(self._convert_from) - 2:
                text.append(("", " and "))
                continue
            if i != len(self._convert_from) - 1:
                text.append(("", ", "))

        text.append(("", " into "))

        for (i, resource) in enumerate(self._convert_to):
            text.append(("class:resource", resource.name))
            if i == len(self._convert_to) - 2:
                text.append(("", " and "))
                continue
            if i != len(self._convert_to) - 1:
                text.append(("", ", "))

        if self._number_of_times != 1:
            text.append(("", " (x"))
            text.append(("class:count", str(self._number_of_times)))
            text.append(("", ")"))

        if "pp" in format_spec:
            return text
        if format_spec.isspace or not format_spec:
            return "".join(e[1] for e in text)
        raise ValueError(f"format spec must be either pp or whitespace, was {format_spec!r}")

    def __repr__(self):
        return f"{self.__class__}({self._convert_from}, {self._convert_to}, {self._number_of_times})"
