from typing import List, Dict, Iterable

from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.prototypes.player_prototype import PlayerPrototype
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_action_ordering_service import ActionOrderingService
from core.baseClasses.base_card import BaseCard
from core.containers.resource_container import ResourceContainer
from core.enums.caverna_enums import ResourceTypeEnum


class ExhaustiveActionOrderingService(ActionOrderingService):
    def __init__(self):
        self._player_prototype: PlayerPrototype = PlayerPrototype()

    def calculated_best_order(
            self,
            actions: ActionChoiceLookup,
            player: Player,
            current_card: BaseCard,
            current_dwarf: Dwarf) -> List[BaseAction]:
        if actions is None:
            raise ValueError
        if player is None:
            raise ValueError
        if c

        score: Dict[List[BaseAction], Dict[ResourceTypeEnum, int]] = {}

        for permutation in self._get_permutations(actions.actions):
            if all(constraint.passes_condition(permutation) for constraint in actions.constraints):
                player_for_permutation: Player = self._player_prototype.clone(player)

                action: BaseAction
                for action in permutation:
                    action.invoke(player, current_card, current_dwarf)