from typing import List

from buisness_logic.actions.place_a_single_tile_action import PlaceASingleTileAction
from buisness_logic.actions.place_a_twin_tile_action import PlaceATwinTileAction
from buisness_logic.actions.place_a_stable_action import PlaceAStableAction
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.enums.caverna_enums import TileTypeEnum
from core.services.base_player_service import BasePlayerService


class PlaceFencesAction(BasePlayerChoiceAction):
    def __init__(self) -> None:
        self._hash = hash(("place fences"))
        BaseAction.__init__(self, "PlaceFencesAction")

    def set_player_choice(
            self,
            player: BasePlayerService,
            unused_dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        if player is None:
            raise ValueError("player cannot be none")

        place_pasture_action = PlaceASingleTileAction(TileTypeEnum.pasture)
        place_twin_pasture_action = PlaceATwinTileAction(TileTypeEnum.pastureTwin)

        fences_to_build_result: ResultLookup[List[BaseAction]] = player \
            .get_player_choice_fences_to_build(
                place_pasture_action,
                place_twin_pasture_action,
                None,
                turn_descriptor)

        if not fences_to_build_result.flag:
            return ResultLookup(errors=fences_to_build_result.errors)
        if len(fences_to_build_result.value) == 0:
            return ResultLookup(True, ActionChoiceLookup([]))

        for action in fences_to_build_result.value:
            if action is place_pasture_action:
                continue
            if action is place_twin_pasture_action:
                continue
            return ResultLookup(errors=f"Player attempted to use invalid fence building action {action}")

        # might be nice to do permutations here, but idc
        return ResultLookup(True, ActionChoiceLookup(fences_to_build_result.value))

    def invoke(self, unused_player, unused_card, unused_dwarf) -> ResultLookup[int]:
        return ResultLookup(True, 0)

    def new_turn_reset(self) -> None:
        pass

    def __format__(self, format_spec: str):
        newline_separator = " "
        try:
            num_spaces = int(format_spec)
            if num_spaces != 0:
                newline_separator = "\r\n" + " " * num_spaces
        except ValueError:
            pass

        text = [
            ("", "Place a "),
            ("", "pasture tile"),
            ("", " (for "),
            ("class:count", "2"),
            ("", " "),
            ("", "wood"),
            ("", f"),{newline_separator}and/or Place a "),
            ("", "pasture twin tile"),
            ("", " (for "),
            ("class:count", "4"),
            ("", " "),
            ("", "wood"),
            ("", ")"),
        ]

        if "pp" in format_spec:
            return text
        return "".join(e[1] for e in text)

    def __hash__(self) -> int:
        return self._hash


class PlaceFencesAndStableAction(BasePlayerChoiceAction):
    def __init__(self) -> None:
        self._hash = hash(("place fences and stable"))
        BaseAction.__init__(self, "PlaceFencesAndStable")

    def set_player_choice(
            self,
            player: BasePlayerService,
            unused_dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        if player is None:
            raise ValueError("player cannot be none")

        place_pasture_action = PlaceASingleTileAction(TileTypeEnum.pasture)
        place_twin_pasture_action = PlaceATwinTileAction(TileTypeEnum.pastureTwin)
        place_stable_action = PlaceAStableAction()

        fences_to_build_result: ResultLookup[List[BaseAction]] = player \
            .get_player_choice_fences_to_build(
                place_pasture_action,
                place_twin_pasture_action,
                place_stable_action,
                turn_descriptor)

        if not fences_to_build_result.flag:
            return ResultLookup(errors=fences_to_build_result.errors)
        if len(fences_to_build_result.value) == 0:
            return ResultLookup(True, ActionChoiceLookup([]))

        for action in fences_to_build_result.value:
            if action is place_pasture_action:
                continue
            if action is place_twin_pasture_action:
                continue
            if action is place_stable_action:
                continue
            return ResultLookup(errors=f"Player attempted to use invalid fence building action {action}")

        # might be nice to do permutations here, but idc
        return ResultLookup(True, ActionChoiceLookup(fences_to_build_result.value))

    def invoke(self, unused_player, unused_card, unused_dwarf) -> ResultLookup[int]:
        return ResultLookup(True, 0)

    def new_turn_reset(self) -> None:
        pass

    def __str__(self) -> str:
        return self.__format__("")

    def __format__(self, format_spec: str):
        newline_separator = ""
        try:
            num_spaces = int(format_spec)
            if num_spaces != 0:
                newline_separator = "\r\n" + " " * num_spaces
        except ValueError:
            pass

        text = [
            ("", "Place a "),
            ("", "pasture tile"),
            ("", " (for "),
            ("class:count", "2"),
            ("", " "),
            ("", "wood"),
            ("", f"), {newline_separator}and/or Place a "),
            ("", "pasture twin tile"),
            ("", " (for "),
            ("class:count", "4"),
            ("", " "),
            ("", "wood"),
            ("", f"), {newline_separator}and/or Place a "),
            ("", "stable"),
            ("", " (for "),
            ("class:count", "1"),
            ("", " "),
            ("", "stone"),
            ("", ")"),
        ]

        if "pp" in format_spec:
            return text
        return "".join(e[1] for e in text)

    def __hash__(self) -> int:
        return self._hash
