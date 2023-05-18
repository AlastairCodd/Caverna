from typing import Dict, List, Callable, Optional

from buisness_logic.actions.breed_animals_action import BreedAnimalsAction
from buisness_logic.actions.feed_dwarves_action import FeedDwarvesAction
from buisness_logic.actions.harvest_field_action import HarvestFieldAction
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.precedes_constraint import PrecedesConstraint
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_constraint import BaseConstraint
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.enums.harvest_type_enum import HarvestTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository
from core.services.base_player_service import BasePlayerService


class ResolveHarvestAction(BasePlayerChoiceAction):
    def __init__(self) -> None:
        self._harvest_type_action_dictionary: Dict[HarvestTypeEnum, Callable[[BasePlayerRepository], ActionChoiceLookup]] = {
            HarvestTypeEnum.NoHarvest: lambda _: ActionChoiceLookup([]),
            HarvestTypeEnum.Harvest: self._handle_full_harvest,
            HarvestTypeEnum.OneFoodPerDwarf: lambda _: ActionChoiceLookup([FeedDwarvesAction(1)]),
            HarvestTypeEnum.EitherFieldPhaseOrBreedingPhase: self._handle_either_field_of_breeding_harvest
        }
        self._harvest_type_this_round: Optional[HarvestTypeEnum] = None
        self._use_harvest_action_instead_of_breeding: Optional[boolean] = None

        self._hash = self._precompute_hash()
        BaseAction.__init__(self, "ResolveHarvestAction", False, False, False)

    def set_player_choice(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        if turn_descriptor is None:
            raise ValueError("Turn Descriptor may not be None")
        self._harvest_type_this_round = turn_descriptor.harvest_type
        harvest_action_choice_lookup: ActionChoiceLookup = self._harvest_type_action_dictionary[turn_descriptor.harvest_type](player)
        return ResultLookup(True, harvest_action_choice_lookup)

    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        result = ResultLookup(True, 0)
        return result

    def new_turn_reset(self) -> None:
        self._harvest_type_this_round = None
        self._use_harvest_action_instead_of_breeding = None

    # noinspection PyUnusedLocal
    def _handle_full_harvest(
            self,
            unused_player: BasePlayerService) -> ActionChoiceLookup:
        harvest_field_action: HarvestFieldAction = HarvestFieldAction()
        feed_dwarves_action: FeedDwarvesAction = FeedDwarvesAction()
        breed_animals_action: BreedAnimalsAction = BreedAnimalsAction()

        actions: List[BaseAction] = [harvest_field_action, feed_dwarves_action, breed_animals_action]

        harvest_field_precedes_feeding_dwarves_constraint: BaseConstraint = PrecedesConstraint(harvest_field_action, feed_dwarves_action)
        feeding_dwarves_precedes_breeding_animals_constraint: BaseConstraint = PrecedesConstraint(feed_dwarves_action, breed_animals_action)

        constraints: List[BaseConstraint] = [harvest_field_precedes_feeding_dwarves_constraint, feeding_dwarves_precedes_breeding_animals_constraint]

        return ActionChoiceLookup(actions, constraints)

    def _handle_either_field_of_breeding_harvest(
            self,
            player: BasePlayerService,
            turn_descriptor) -> ActionChoiceLookup:
        if player is None:
            raise ValueError("Player may not be None")
        self._use_harvest_action_instead_of_breeding: bool = player.get_player_choice_use_harvest_action_instead_of_breeding(turn_descriptor)

        result: ActionChoiceLookup
        if self._use_harvest_action_instead_of_breeding:
            harvest_field_action: HarvestFieldAction = HarvestFieldAction()
            feed_dwarves_action: FeedDwarvesAction = FeedDwarvesAction()

            actions: List[BaseAction] = [harvest_field_action, feed_dwarves_action]

            harvest_field_precedes_feeding_dwarves_constraint: BaseConstraint = PrecedesConstraint(harvest_field_action, feed_dwarves_action)

            return ActionChoiceLookup(actions, [harvest_field_precedes_feeding_dwarves_constraint])
        else:
            feed_dwarves_action: FeedDwarvesAction = FeedDwarvesAction()
            breed_animals_action: BreedAnimalsAction = BreedAnimalsAction()

            actions: List[BaseAction] = [feed_dwarves_action, breed_animals_action]

            feeding_dwarves_precedes_breeding_animals_constraint: BaseConstraint = PrecedesConstraint(feed_dwarves_action, breed_animals_action)

            result = ActionChoiceLookup(actions, [feeding_dwarves_precedes_breeding_animals_constraint])
        return result

    def __repr__(self) -> str:
        return "ResolveHarvestAction()"

    def __str__(self) -> str:
        if self._harvest_type_this_round is None:
            return "Resolve harvest"
        if self._harvest_type_this_round == HarvestTypeEnum.Harvest:
            return "Resolve full harvest"
        if self._harvest_type_this_round == HarvestTypeEnum.OneFoodPerDwarf:
            return "Resolve harvest by feeding each dwarf one food"
        if self._harvest_type_this_round == HarvestTypeEnum.NoHarvest:
            return "Resolve non-harvest harvest"

        if self._use_harvest_action_instead_of_breeding is None:
            return "Resolve harvest with either farming or breeding animals"
        if self._use_harvest_action_instead_of_breeding:
            return "Resolve harvest where player chose to farm"
        return "Resolve harvest where player chose to breed animals"

    def _precompute_hash(self) -> int:
        return hash(self.__repr__())

    def __hash__(self) -> int:
        return self._hash
