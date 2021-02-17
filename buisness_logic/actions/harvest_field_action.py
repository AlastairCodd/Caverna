from typing import List

from buisness_logic.effects.allow_farming_effect import AllowFarmingEffect
from buisness_logic.services.base_receive_event_service import BaseReceiveEventService
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.repositories.base_player_repository import BasePlayerRepository


class HarvestFieldAction(BaseAction, BaseReceiveEventService):
    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        if player is None:
            raise ValueError("Player may not be None")
        allow_farming_effects: List[AllowFarmingEffect] = player.get_effects_of_type(AllowFarmingEffect)

        success: bool = True
        count: int = 0
        errors: List[str] = []

        for effect in allow_farming_effects:
            if effect.planted_resource_type is not None:
                pop_result: ResultLookup[int] = effect.pop_resource(player)

                success &= pop_result.flag
                errors.extend(pop_result.errors)

                if pop_result.flag:
                    count += pop_result.value

        result: ResultLookup[int] = ResultLookup(success, count, errors)
        return result

    def new_turn_reset(self) -> None:
        pass