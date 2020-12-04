from typing import List, Iterable, Dict

from buisness_logic.actions.breed_animals_action import BreedAnimalsAction
from buisness_logic.actions.placeATileAction import PlaceATileAction
from buisness_logic.actions.place_a_stable_action import PlaceAStableAction
from buisness_logic.actions.receiveAction import ReceiveAction
from buisness_logic.actions.sowAction import SowAction
from buisness_logic.actions.upgrade_all_weapons_action import UpgradeAllWeaponsAction
from buisness_logic.actions.upgrade_dwarf_weapon_action import UpgradeDwarfWeaponAction
from buisness_logic.tiles.dwelling import Dwelling
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.precedes_constraint import PrecedesConstraint
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_constraint import BaseConstraint
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.enums.caverna_enums import ResourceTypeEnum, TileTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository
from core.services.base_player_service import BasePlayerService


class GoOnAnExpeditionAction(BasePlayerChoiceAction):
    def __init__(
            self,
            level: int) -> None:
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
            8: [PlaceAStableAction()],
            9: [PlaceATileAction(TileTypeEnum.tunnel),
                PlaceATileAction(TileTypeEnum.pasture)],
            10: [PlaceATileAction(TileTypeEnum.pastureTwin),
                 ReceiveAction({ResourceTypeEnum.cow: 1})],
            11: [PlaceATileAction(TileTypeEnum.meadow),
                 PlaceATileAction(TileTypeEnum.furnishedDwelling,
                                  specific_tile_generation_method=Dwelling,
                                  override_cost={ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 1})],
            12: [PlaceATileAction(TileTypeEnum.field),
                 SowAction()],
            14: [PlaceATileAction(TileTypeEnum.cavern),
                 BreedAnimalsAction(maximum=2)]}

        self._upgrade_dwarf_weapon_action: BaseAction = UpgradeDwarfWeaponAction()

        self._chosen_actions_and_levels: Dict[BaseAction, int] = {}

    def set_player_choice(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        if player is None:
            raise ValueError(str(player))

        possible_expedition_rewards = []
        possible_expedition_rewards_and_levels: Dict[BaseAction, int] = {}
        for level in self._expedition_actions:
            for action in self._expedition_actions[level]:
                possible_expedition_rewards.append(action)
                possible_expedition_rewards_and_levels[action] = level

        chosen_expedition_actions: ResultLookup[List[BaseAction]] = player.get_player_choice_expedition_reward(
            possible_expedition_rewards,
            self._level,
            turn_descriptor)

        errors: List[str] = []
        errors.extend(chosen_expedition_actions.errors)

        actions: List[BaseAction] = [self._upgrade_dwarf_weapon_action]
        constraints: List[BaseConstraint] = [PrecedesConstraint(self, self._upgrade_dwarf_weapon_action)]

        if chosen_expedition_actions.flag:
            if len(chosen_expedition_actions.value) != self._level:
                errors.append(f"Player attempted to choose {len(chosen_expedition_actions.value)} actions, when only {self._level} are allowed")
            else:
                for action in chosen_expedition_actions.value:
                    if action in possible_expedition_rewards:
                        self._chosen_actions_and_levels[action] = possible_expedition_rewards_and_levels[action]

                        after_expedition_constraint: BaseConstraint = PrecedesConstraint(self, action)
                        constraints.append(after_expedition_constraint)
                        actions.append(action)

                        before_dwarf_level_constraint: BaseConstraint = PrecedesConstraint(action, self._upgrade_dwarf_weapon_action)
                        constraints.append(before_dwarf_level_constraint)
                    else:
                        errors.append(f"player attempted to perform expedition action {action} that does not exist")

        result: ResultLookup[ActionChoiceLookup]
        if len(errors) == 0:
            action_choice_lookup: ActionChoiceLookup = ActionChoiceLookup(actions, constraints)
            result = ResultLookup(True, action_choice_lookup)
        else:
            result = ResultLookup(errors=errors)
        return result

    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        if player is None:
            raise ValueError("Player may not be none")
        if current_dwarf is None:
            raise ValueError("Current dwarf may not be none")
        if len(self._chosen_actions_and_levels) == 0:
            raise ValueError("Must choose ")

        errors: List[str] = []

        if current_dwarf.has_weapon:
            for action in self._chosen_actions_and_levels:
                dwarf_level_required_for_action: int = self._chosen_actions_and_levels[action]
                if dwarf_level_required_for_action > current_dwarf.weapon_level:
                    errors.append(f"Tried to perform expedition {action} of level {dwarf_level_required_for_action}, but dwarf weapon was of level "
                                  f"{current_dwarf.weapon_level}")

        result: ResultLookup[int] = ResultLookup(True, 1) if len(errors) == 0 else ResultLookup(errors=errors)
        return result

    def new_turn_reset(self) -> None:
        self._chosen_actions_and_levels.clear()
