from collections import Counter
from functools import reduce
from typing import Dict, List

from buisness_logic.effects.food_effects import FoodPerDwarfEffect, BaseFoodEffect, FoodGlobalEffect
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.enums.caverna_enums import ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository
from core.services.base_player_service import BasePlayerService


class FeedDwarvesAction(BasePlayerChoiceAction):
    def __init__(
            self,
            amount_of_food_required_per_dwarf: int = 2) -> None:
        if amount_of_food_required_per_dwarf <= 0:
            raise ValueError("Amount of Food Required per dwarf must be positive")
        self._amount_of_food_required_per_dwarf: int = amount_of_food_required_per_dwarf
        self._effects_to_use: List[BaseFoodEffect] = []
        BasePlayerChoiceAction.__init__(self, "FeedDwarvesAction")

    def set_player_choice(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        if player is None:
            raise ValueError("Player may not be None")
        if turn_descriptor is None:
            raise ValueError("Turn Descriptor may not be None")

        effects_to_use_result: ResultLookup[List[BaseFoodEffect]] = player.get_player_choice_effect_to_use_for_feeding_dwarves(turn_descriptor)

        result: ResultLookup[ActionChoiceLookup]
        if effects_to_use_result.flag:
            self._effects_to_use = effects_to_use_result.value
            result = ResultLookup(True, ActionChoiceLookup([]))
        else:
            result = ResultLookup(errors=effects_to_use_result.errors)
        return result

    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        if player is None:
            raise ValueError("Player may not be None")

        # you may feed exactly 1 dwarf with 1 wood or 1 stone or 2 ore
        # discount of 1 food per donkey in a mine

        errors: List[str] = []

        has_effects_result: ResultLookup[bool] = self._does_player_have_effects(player)

        errors.extend(has_effects_result.errors)

        resources_per_dwarf: List[Dict[ResourceTypeEnum, int]] = []
        for dwarf in player.dwarves:
            amount_of_food_required = self._amount_of_food_required_per_dwarf if dwarf.is_adult else 1
            resources_per_dwarf.append({ResourceTypeEnum.food: amount_of_food_required})

        per_dwarf_effects: List[FoodPerDwarfEffect] = []

        for effect in per_dwarf_effects:
            effect.invoke(resources_per_dwarf)

        # noinspection PyTypeChecker
        resources_required: Dict[ResourceTypeEnum, int] = dict(reduce(lambda m, n: Counter(m) + Counter(n), resources_per_dwarf))

        global_effects: List[FoodGlobalEffect] = []
        for effect in global_effects:
            effect.invoke(resources_required, player)

        resources_to_take: Dict[ResourceTypeEnum, int] = dict(resources_required)
        resources_to_give: Dict[ResourceTypeEnum, int] = {}

        for resource, amount_of_resource_required in resources_required.items():
            amount_of_resource_player_has: int = player.get_resources_of_type(resource)

            if resource == ResourceTypeEnum.food:
                food_deficit: int = amount_of_resource_required - amount_of_resource_player_has
                if food_deficit > 0:
                    resources_to_take[resource] = amount_of_resource_player_has
                    resources_to_give[ResourceTypeEnum.begging_marker] = food_deficit * 3
            elif amount_of_resource_required > amount_of_resource_player_has:
                errors.append(f"Effect was used to attempt to feed dwarves with {amount_of_resource_required}, only had {amount_of_resource_player_has}")

        result: ResultLookup[int]
        if len(errors) == 0:
            success: bool = player.take_resources(resources_to_take)
            if len(resources_to_give) > 0 and success:
                success = player.give_resources(resources_to_give)

            result = ResultLookup(success, sum(resources_to_take.values()))
        else:
            result = ResultLookup(errors=errors)
        return result

    def new_turn_reset(self) -> None:
        self._effects_to_use.clear()

    def __repr__(self) -> str:
        return "FeedDwarvesAction()" if self._amount_of_food_required_per_dwarf == 2 else f"FeedDwarvesAction({self._amount_of_food_required_per_dwarf})"

    def _does_player_have_effects(
            self,
            player: BasePlayerRepository) -> ResultLookup[bool]:
        errors: List[str] = []

        if len(self._effects_to_use) > 0:
            effects_player_has: List[BaseFoodEffect] = player.get_effects_of_type(BaseFoodEffect)

            effect: BaseFoodEffect
            for effect in self._effects_to_use:
                if effect not in effects_player_has:
                    warning: str = f"Player wanted to use effect {effect} times, but does not posses it"
                    errors.append(warning)

        success: bool = len(errors) == 0
        return ResultLookup(success, success, errors)

    def __hash__(self) -> int:
        return hash(self.__repr__())
