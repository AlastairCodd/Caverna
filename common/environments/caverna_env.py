from typing import Tuple, Dict, List, Optional
# from gym import Env
from numpy import array, concatenate, random

from InquirerPy.utils import color_print

from buisness_logic.services.turn_execution_service import TurnExecutionService
from common.defaults.card_default import CardDefault
from common.services.caverna_state_service import CavernaStateService
from common.services.levelled_card_service import LevelledCardService
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from common.defaults.players_default import PlayersDefault
from common.entities.dwarf import Dwarf
from common.forges.tile_forge import TileForge
from core.baseClasses.base_resource_containing_card import BaseResourceContainingCard
from core.baseClasses.base_tile import BaseTile
from core.constants import game_constants
from core.enums.harvest_type_enum import HarvestTypeEnum
from core.services.base_player_service import BasePlayerService
from common.services.point_calculation_service import PointCalculationService
from core.baseClasses.base_card import BaseCard


class CavernaEnv(object):
    """Environment for running caverna games"""
    def __init__(
            self,
            number_of_players: int = 7,
            players_default: Optional[PlayersDefault] = None,
            card_default: Optional[CardDefault] = None,
            tile_forge: Optional[TileForge] = None):
        """Ctor

        Params: numberOfPlayers: int. Must be between 1 and 7 (inclusive)."""
        if number_of_players < 1:
            raise IndexError("numberOfPlayers")
        if number_of_players > 7:
            raise IndexError("numberOfPlayers")
        self._number_of_players = number_of_players

        self._players_default: PlayersDefault = PlayersDefault(self._number_of_players) if players_default is None else players_default
        self._card_default: CardDefault = CardDefault(self._number_of_players) if card_default is None else card_default
        self._levelled_card_service: LevelledCardService = LevelledCardService()
        self._tile_forge: TileForge = TileForge() if tile_forge is None else TileForge

        self._harvest_types_by_round: List[HarvestTypeEnum] = []

        self._cards_to_reveal: List[BaseCard] = []
        self._tiles: List[BaseTile] = []
        self._state: CavernaStateService = CavernaStateService([], [])

        self._turn_execution_service: TurnExecutionService = TurnExecutionService()
        self._point_calculation_service: PointCalculationService = PointCalculationService()

        self._logging = True

    def reset(self) -> array:
        """Resets the environment

        Returns: the observation of the game state"""
        players = self._players_default.assign([])

        starting_cards: List[BaseCard] = self._card_default.get_cards()
        self._cards_to_reveal = self._levelled_card_service.get_cards()

        self._tiles = self._tile_forge.create_all_tiles()

        self._harvest_types_by_round = [HarvestTypeEnum.Harvest for _ in range(game_constants.number_of_rounds)]
        red_question_mark_harvest_round_indexes: List[int] = list(sorted(random.choice(list(range(5, 12)), 3, replace=False)))
        self._harvest_types_by_round[0] = HarvestTypeEnum.NoHarvest
        self._harvest_types_by_round[1] = HarvestTypeEnum.NoHarvest
        self._harvest_types_by_round[3] = HarvestTypeEnum.OneFoodPerDwarf
        self._harvest_types_by_round[red_question_mark_harvest_round_indexes[0]] = HarvestTypeEnum.NoHarvest
        self._harvest_types_by_round[red_question_mark_harvest_round_indexes[1]] = HarvestTypeEnum.OneFoodPerDwarf
        self._harvest_types_by_round[red_question_mark_harvest_round_indexes[2]] = HarvestTypeEnum.EitherFieldPhaseOrBreedingPhase

        self._state: CavernaStateService = CavernaStateService(players, starting_cards)
        self._state.increment_round_index(self._cards_to_reveal[0], self._harvest_types_by_round[0], logging=self._logging)
        self._state.get_next_player(logging=self._logging)

        return self.observe()

    def render(self, mode='human'):
        pass

    def seed(self, seed: int) -> None:
        """Seeds the environment.
        Args:
          seed: Value to use as seed for the environment.
        """
        random.seed(seed)

    def step(self) -> Tuple[array, float, bool, Dict]:
        """Takes an action service (either the output of a network or a delayed decision maker)
        and applies the actions to get the next state

        Returns:
            array: the observation of the game state
            float: the reward for the last action
            bool: whether or not the game has finished
            dict: additional debug information"""
        current_player: BasePlayerService = self._state.current_player
        player_points_at_turn_start: int = self._point_calculation_service.calculate_points(current_player)

        turn_descriptor: TurnDescriptorLookup = TurnDescriptorLookup(
            self._state.cards,
            self._tiles,
            self._state.turn_index,
            self._state.round_index,
            self._state.round_harvest_type)

        color_print(
            formatted_text=[("", f"{current_player.descriptor}'s turn (player {current_player.turn_index+1}/{self._number_of_players}, dwarf {self._state.turn_index + 1}):")],
            style={"": "underline"},
        )

        turn_result: ResultLookup[int] = self._turn_execution_service.take_turn(
            current_player,
            self._state.is_current_players_final_turn,
            turn_descriptor)

        for error in turn_result.errors:
            print(format(error, "4"))

        next_player_result: ResultLookup[BasePlayerService] = self._state.get_next_player(logging=self._logging)

        has_game_finished: bool = False

        if not next_player_result.flag:
            next_round_index = self._state.round_index + 1

            if next_round_index < game_constants.number_of_rounds:
                card_to_reveal: BaseCard = self._cards_to_reveal[next_round_index]
                harvest_type: HarvestTypeEnum = self._harvest_types_by_round[next_round_index]

                self._state.increment_round_index(card_to_reveal, harvest_type, logging=self._logging)

                next_player_result = self._state.get_next_player(logging=self._logging)
            else:
                has_game_finished = True

        player_points_after_action: int = self._point_calculation_service.calculate_points(current_player)
        reward: int = player_points_after_action - player_points_at_turn_start
        return array([]), reward, has_game_finished, {}

    def observe(self) -> array:
        observation: array = array([])

        return observation

    def _observe_player(self, player: BasePlayerService) -> array:
        player_observation = array(player.resources)
        for i in range(6):
            dwarf = player.dwarves[i] if i <= len(player.dwarves) - 1 else None
            player_observation = concatenate(player_observation, self._observe_dwarf(dwarf), axis=None)

        return player_observation

    def _observe_dwarf(self, dwarf: Dwarf) -> array:
        if dwarf is None:
            return array([0, 0, 0, 0])
        dwarf_observation = array([dwarf.is_active, dwarf.is_adult, dwarf.weapon.level, dwarf.current_card_id])
        return dwarf_observation
