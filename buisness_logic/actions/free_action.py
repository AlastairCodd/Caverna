from buisness_logic.effects.free_action_effects import FreeActionEffect
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.enums.caverna_enums import ResourceTypeEnum
from core.exceptions.invalid_operation_error import InvalidOperationError
from core.repositories.base_player_repository import BasePlayerRepository
from core.services.base_player_service import BasePlayerService


class FreeAction(BasePlayerChoiceAction):
    def __init__(self) -> None:
        self._hash = self._precompute_hash()
        BasePlayerChoiceAction.__init__(self, "FreeAction", False, False, False)
        self._actions_to_take: list[BaseAction] = []

    def set_player_choice(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        if player is None:
            raise ValueError("Player may not be None")
        if turn_descriptor is None:
            raise ValueError("Turn Descriptor may not be none")
        self._actions_to_take = player.get_player_choice_free_actions_to_use(turn_descriptor)

        return ResultLookup(True, ActionChoiceLookup(self._actions_to_take))

    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        if len(self._actions_to_take) == 0:
            return ResultLookup(True, 0)

        # validate that the player actually has the actions they want to use
        # NOTE: since the only free-actions are in the EntryLevelDwelling, this check
        #       could be done when the player chooses what they're doing. but i want
        #       to optimise get_effects_of_type so this stays for now. it's also more
        #       flexible
        possible_actions = [effect.action for effect in player.get_effects_of_type(FreeActionEffect)]

        success = True
        errors = []
        for action in self._actions_to_take:
            if action not in possible_actions:
                success = False
                errors.append(f"Attempted to take free action {action} that was not possible")
        return ResultLookup(True, 0, errors=errors)

    def new_turn_reset(self) -> None:
        pass

    def __repr__(self) -> str:
        return "FreeAction()"

    def _precompute_hash(self) -> int:
        return hash(self.__repr__())

    def __hash__(self) -> int:
        return self._hash
