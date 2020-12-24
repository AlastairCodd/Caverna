from typing import Optional, List, Dict

from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.tile_entity import TileEntity
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_effect import BaseEffect
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.enums.caverna_enums import ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository
from core.services.base_player_service import BasePlayerService


class PlaceAStableAction(BasePlayerChoiceAction):
    def __init__(
            self,
            override_cost: Optional[Dict[ResourceTypeEnum, int]] = None) -> None:
        self._override_cost: Optional[Dict[ResourceTypeEnum, int]] = override_cost
        # TODO: Potentially include this.
        # self._tile_service: TileService = TileService()

        self._location_to_place_stable: Optional[int] = None
        self._cost_for_stable: Optional[Dict[ResourceTypeEnum, int]] = None
        self._effects_to_use: List[BaseEffect] = []

    def set_player_choice(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        # TODO: Implement this
        self._location_to_place_stable = 1
        self._cost_for_stable = self._override_cost if self._override_cost is not None else {ResourceTypeEnum.stone: 1}
        pass

    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        if player is None:
            raise ValueError("Player may not be null")
        if self._location_to_place_stable is None:
            raise ValueError("Must chose valid place for stable")

        successes: int = 0
        errors: List[str] = []

        for effect in self._effects_to_use:
            does_player_have_effect: bool = effect in player.effects
            if not does_player_have_effect:
                errors.append("Player does not have access to effect")

        tile_at_location: TileEntity = player.get_tile_at_location(self._location_to_place_stable)
        if tile_at_location.has_stable:
            errors.append(f"Tile at location {self._location_to_place_stable} already has a stable.")
        else:
            can_player_afford_tile: int = player.has_more_resources_than(self._cost_for_stable)
            if can_player_afford_tile:
                successfully_paid: bool = player.take_resources(self._cost_for_stable)
                if successfully_paid:
                    number_of_resources: int = sum([x for x in self._cost_for_stable.values()])
                    successes += number_of_resources
                    successfully_placed_stable: bool = tile_at_location.give_stable()
                    if successfully_placed_stable:
                        successes += 1
                    else:
                        errors.append(f"DEV ERROR: Could not place stable on tile. Initial Check Passed.")
                else:
                    errors.append(f"DEV ERROR: Player was unable to pay for stable. Initial Check Passed.")
            else:
                errors.append(f"Player cannot afford to pay to build stable.")

        success: bool = len(errors) == 0
        result: ResultLookup[int] = ResultLookup(success, successes, errors)
        return result

    def new_turn_reset(self) -> None:
        self._cost_for_stable = None
        self._location_to_place_stable = None
        self._effects_to_use = []
