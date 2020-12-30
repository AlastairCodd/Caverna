from abc import ABCMeta
from typing import Dict, List

from buisness_logic.effects.receive_when_receiving_effect import ReceiveWhenReceivingEffect
from common.entities.result_lookup import ResultLookup
from core.enums.caverna_enums import ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository


class BaseReceiveEventService(metaclass=ABCMeta):
    def _give_player_resources(
            self,
            player: BasePlayerRepository,
            resources: Dict[ResourceTypeEnum, int]) -> ResultLookup[int]:
        receive_conditionally_effects: List[ReceiveWhenReceivingEffect] = player.get_effects_of_type(ReceiveWhenReceivingEffect)
        resources_to_receive: Dict[ResourceTypeEnum, int] = resources.copy()

        # currently only two ReceiveWhenReceivingEffects exist, with no overlap. If that changes, this will need rewriting.
        for effect in receive_conditionally_effects:
            new_resources: Dict[ResourceTypeEnum, int] = effect.invoke(resources)
            for resource in new_resources:
                if resource in resources_to_receive:
                    resources_to_receive[resource] += new_resources[resource]
                else:
                    resources_to_receive[resource] = new_resources[resource]

        did_receive_resources_successfully: bool = player.give_resources(resources_to_receive)

        result: ResultLookup[int] = ResultLookup(True, sum(resources_to_receive.values())) \
            if did_receive_resources_successfully \
            else ResultLookup(False, 0, "Did not receive resources successfully")

        return result
