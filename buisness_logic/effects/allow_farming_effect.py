from typing import Dict, Optional, List

from buisness_logic.actions.receive_action import ReceiveAction
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_effect import BaseEffect
from core.enums.caverna_enums import ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository


class AllowFarmingEffect(BaseEffect):
    def __init__(
            self,
            planted_resource_type: Optional[ResourceTypeEnum] = None,
            planted_resource_amount: int = 0) -> None:
        self._resource_type_rewards: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.grain: 3,
            ResourceTypeEnum.veg: 2}

        self._planted_resource_type: Optional[ResourceTypeEnum] = planted_resource_type
        self._planted_resource_amount: int = planted_resource_amount

    @property
    def planted_resource_type(self) -> Optional[ResourceTypeEnum]:
        return self._planted_resource_type

    @property
    def planted_resource_amount(self) -> int:
        return self._planted_resource_amount

    def plant_resource(
            self,
            player: BasePlayerRepository,
            resource_type: ResourceTypeEnum) -> ResultLookup[bool]:
        if player is None:
            raise ValueError("Player may not be None")
        if resource_type not in self._resource_type_rewards:
            raise ValueError(f"Resource {resource_type} cannot be planted on this tile.")

        errors: List[str] = []

        if self._planted_resource_type is not None:
            errors.append("Tile has already been planted.")

        if not player.has_more_resources_than({resource_type: 1}):
            errors.append(f"Player does not have sufficient resources to plant {resource_type}")

        result: ResultLookup[bool]
        success: bool = len(errors) == 0

        if success:
            success &= player.take_resource(resource_type, 1)
            self._planted_resource_type = resource_type
            self._planted_resource_amount = self._resource_type_rewards[resource_type]

            result = ResultLookup(True, True)
        else:
            result = ResultLookup(errors=errors)
        return result

    def pop_resource(
            self,
            player: BasePlayerRepository) -> ResultLookup[int]:
        if player is None:
            raise ValueError("Player cannot be None")

        result: ResultLookup[bool]
        if self._planted_resource_type is None:
            result = ResultLookup(errors="Tile has nothing planted on it")
        else:
            receive_action: ReceiveAction = ReceiveAction({self._planted_resource_type: 1})

            # noinspection PyTypeChecker
            result: ResultLookup[int] = receive_action.invoke(player, None, None)

            self._planted_resource_amount -= 1
            if self._planted_resource_amount == 0:
                self._planted_resource_type = None

        return result
