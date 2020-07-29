from typing import List, Iterable, Dict

from buisness_logic.actions.breed_animals_action import BreedAnimalsAction
from buisness_logic.actions.placeATileAction import PlaceATileAction
from buisness_logic.actions.receiveAction import ReceiveAction
from buisness_logic.actions.sowAction import SowAction
from buisness_logic.actions.upgrade_all_weapons_action import UpgradeAllWeaponsAction
from buisness_logic.tiles.dwelling import Dwelling
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from core.repositories.base_player_repository import BasePlayerRepository
from core.services.base_player_service import BasePlayerService
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.enums.caverna_enums import ResourceTypeEnum, TileTypeEnum
from core.enums.harvest_type_enum import HarvestTypeEnum


class GoOnAnExpeditionAction(BasePlayerChoiceAction):
    def __init__(self, level: int) -> None:
        if level < 1:
            raise ValueError(f"Level must be positive: (level={level})")
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
                                  override_cost={ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 1})],
            12: [PlaceATileAction(TileTypeEnum.field),
                 SowAction()],
            14: [PlaceATileAction(TileTypeEnum.cavern),
                 BreedAnimalsAction(maximum=2)]

        }

    def set_player_choice(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            cards: List[BaseCard],
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) -> ResultLookup[ActionChoiceLookup]:
        if player is None:
            raise ValueError(str(player))
        weapon_level = dwarf.weapon_level

        possible_expedition_rewards: List[BaseAction] = []
        for level, actions_available_for_level in self._expedition_actions.items():
            if level <= weapon_level:
                for action in actions_available_for_level:
                    possible_expedition_rewards.append(action)

        chosen_expedition_actions: ResultLookup[List[BaseAction]] = player.get_player_choice_expedition_reward(
            possible_expedition_rewards,
            self._level,
            turn_index,
            round_index,
            harvest_type)

        result: ResultLookup[ActionChoiceLookup]

        if chosen_expedition_actions.flag:
            data: ActionChoiceLookup = ActionChoiceLookup(chosen_expedition_actions.value)
            result = ResultLookup(True, data, chosen_expedition_actions.errors)
        else:
            result = ResultLookup(errors=chosen_expedition_actions.errors)
        return result

    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        if current_dwarf is None:
            raise ValueError("dwarf cannot be none -- should be levelled up")

        result: ResultLookup[int]
        if current_dwarf.has_weapon:
            result = current_dwarf.weapon.increase_level()
        else:
            result = ResultLookup(True, 0, "Dwarf does not have a weapon")
        return result

    def new_turn_reset(self):
        pass
