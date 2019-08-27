from typing import List, Iterable, Dict

from buisness_logic.actions.breed_animals_action import BreedAnimalsAction
from buisness_logic.actions.placeATileAction import PlaceATileAction
from buisness_logic.actions.receiveAction import ReceiveAction
from buisness_logic.actions.sowAction import SowAction
from buisness_logic.actions.upgrade_all_weapons_action import UpgradeAllWeaponsAction
from buisness_logic.tiles.dwelling import Dwelling
from common.entities.dwarf import Dwarf
from common.entities.player import Player
from core.baseClasses.base_action import BaseAction
from core.containers.resource_container import ResourceContainer
from core.enums.caverna_enums import ResourceTypeEnum, TileTypeEnum


class GoOnAnExpeditionAction(BaseAction):
    def __init__(self, level: int):
        if level < 1 or level > 4:
            raise ValueError("level")
        self._level = level
        self._expedition_actions: Dict[int, Iterable[BaseAction]] = {
            1: [UpgradeAllWeaponsAction(),
                ReceiveAction({ResourceTypeEnum.wood: 1}),
                ReceiveAction({ResourceTypeEnum.dog: 1})],
            2: [ReceiveAction({ResourceTypeEnum.grain: 1}),
                ReceiveAction({ResourceTypeEnum.sheep: 1})],
            3: [ReceiveAction({ResourceTypeEnum.stone: 1}),
                ReceiveAction({ResourceTypeEnum.donkey: 1})],
            4: [ReceiveAction({ResourceTypeEnum.veg: 1}),
                ReceiveAction({ResourceTypeEnum.ore: 2})],
            5: [ReceiveAction({ResourceTypeEnum.boar: 1})],
            6: [ReceiveAction({ResourceTypeEnum.coin: 2})],
            7: [PlaceATileAction(TileTypeEnum.furnishedCavern)],
            8: [PlaceATileAction(TileTypeEnum.stable)],
            9: [PlaceATileAction(TileTypeEnum.tunnel),
                PlaceATileAction(TileTypeEnum.pasture)],
            10: [PlaceATileAction(TileTypeEnum.pastureTwin),
                 ReceiveAction({ResourceTypeEnum.cow: 1})],
            11: [PlaceATileAction(TileTypeEnum.meadow),
                 PlaceATileAction(TileTypeEnum.furnishedDwelling,
                                  specific_tile=Dwelling(),
                                  cost={ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 1})],
            12: [PlaceATileAction(TileTypeEnum.field),
                 SowAction()],
            14: [PlaceATileAction(TileTypeEnum.cavern),
                 BreedAnimalsAction(maximum_=2)]

        }

    def invoke(self, player: Player, active_card: ResourceContainer, current_dwarf: Dwarf) -> bool:
        if player is None:
            raise ValueError(str(player))
        weapon_level = current_dwarf.weapon_level

        possible_expedition_rewards: List[BaseAction] = []
        for level, actions_available_for_level in self._expedition_actions.items():
            if level <= weapon_level:
                for action in actions_available_for_level:
                    possible_expedition_rewards.append(action)

        player_choice: List[BaseAction] = player.get_player_choice_expedition_reward(possible_expedition_rewards)

        raise NotImplementedError()

    def new_turn_reset(self):
        pass
