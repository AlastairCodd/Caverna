from typing import Tuple, Dict, List, Optional
# from gym import Env
from numpy import array, concatenate, random

from buisness_logic.services.turn_execution_service import TurnExecutionService
from common.defaults.card_default import CardDefault
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
    def __init__(self, number_of_players: int = 7):
        """Ctor
        
        Params: numberOfPlayers: int. Must be between 1 and 7 (inclusive)."""
        if number_of_players < 1:
            raise IndexError("numberOfPlayers")
        if number_of_players > 7:
            raise IndexError("numberOfPlayers")
        self._number_of_players = number_of_players

        self._players_default: PlayersDefault = PlayersDefault(self._number_of_players)
        self._card_default: CardDefault = CardDefault(self._number_of_players)
        self._levelled_card_service: LevelledCardService = LevelledCardService()
        self._tile_forge: TileForge = TileForge()

        self._players: List[BasePlayerService] = []
        self._turn_index: int = 0
        self._round_index: int = 0
        self._harvest_type_for_round: HarvestTypeEnum = HarvestTypeEnum.NoHarvest
        self._harvest_types_by_round: List[HarvestTypeEnum] = []

        # noinspection PyTypeChecker
        self._current_player: BasePlayerService = None
        self._is_current_players_final_turn: bool = False
        # noinspection PyTypeChecker
        self._starting_player: BasePlayerService = None
        self._player_turn_order: List[BasePlayerService] = []

        self._cards: List[BaseCard] = []
        self._cards_to_reveal: List[BaseCard] = []
        self._tiles: List[BaseTile] = []

        self._turn_execution_service: TurnExecutionService = TurnExecutionService()
        self._point_calculation_service: PointCalculationService = PointCalculationService()
    
    def reset(self) -> array:
        """Resets the environment
        
        Returns: the observation of the game state"""
        self._players: List[BasePlayerService] = self._players_default.assign([])
        self._harvest_types_by_round = [HarvestTypeEnum.Harvest for _ in range(game_constants.number_of_rounds)]

        self._cards = self._card_default.get_cards()
        self._cards_to_reveal = self._levelled_card_service.get_cards()
        self._cards.extend(self._cards_to_reveal)

        self._tiles = self._tile_forge.create_all_tiles()

        self._starting_player = self._players[0]

        red_question_mark_harvest_round_indexes: List[int] = list(sorted(random.choice(list(range(5, 12)), 3, replace=False)))
        self._harvest_types_by_round[0] = HarvestTypeEnum.NoHarvest
        self._harvest_types_by_round[1] = HarvestTypeEnum.NoHarvest
        self._harvest_types_by_round[3] = HarvestTypeEnum.OneFoodPerDwarf
        self._harvest_types_by_round[red_question_mark_harvest_round_indexes[0]] = HarvestTypeEnum.NoHarvest
        self._harvest_types_by_round[red_question_mark_harvest_round_indexes[1]] = HarvestTypeEnum.OneFoodPerDwarf
        self._harvest_types_by_round[red_question_mark_harvest_round_indexes[2]] = HarvestTypeEnum.EitherFieldPhaseOrBreedingPhase

        self._round_index = -1
        self._increment_round_index()

        self._player_turn_order = self._create_player_turn_order()
        self._current_player, self._is_current_players_final_turn = self._get_next_player_in_turn()

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
        player_points_at_turn_start: int = self._point_calculation_service.calculate_points(self._current_player)

        turn_descriptor: TurnDescriptorLookup = TurnDescriptorLookup(
            self._cards,
            self._tiles,
            self._turn_index,
            self._round_index,
            self._harvest_type_for_round)

        turn_result: ResultLookup[int] = self._turn_execution_service.take_turn(self._current_player, turn_descriptor)

        for error in turn_result.errors:
            print(error)

        next_player: Optional[BasePlayerService]
        is_final_turn: Optional[bool]
        next_player, is_final_turn = self._get_next_player_in_turn()

        if next_player is None:
            next_player = self._increment_turn_index()
            is_final_turn = False

        has_game_finished: bool = next_player is None
        if not has_game_finished:
            self._current_player = next_player
            self._is_current_players_final_turn = is_final_turn

        player_points_after_action: int = self._point_calculation_service.calculate_points(self._current_player)
        reward: int = player_points_after_action - player_points_at_turn_start
        return array([]), reward, has_game_finished, {}

    def observe(self) -> array:
        observation: array = array([])
        
        return observation

    def _get_next_player_in_turn(self) -> Tuple[Optional[BasePlayerService], Optional[bool]]:
        if any(self._player_turn_order):
            player: BasePlayerService = self._player_turn_order.pop(0)
            number_of_remaining_dwarves: int = len([d for d in player.dwarves if d.is_adult and not d.is_active])
            is_final_turn: bool = number_of_remaining_dwarves == 1

            print(f"{player.descriptor}{' final' if is_final_turn else ''} turn")
            return player, is_final_turn
        else:
            return None, None

    def _create_player_turn_order(self) -> List[BasePlayerService]:
        player_turn_order: List[BasePlayerService] = []
        for player in self._get_players_starting_at(self._starting_player.id):
            if any(d for d in player.dwarves if d.is_adult and not d.is_active):
                player_turn_order.append(player)

        return player_turn_order
    
    def _get_players_starting_at(self, starting_index: int) -> List[BasePlayerService]:
        result = self._players[starting_index:] + self._players[:starting_index-1]
        return result

    def _increment_turn_index(self) -> Optional[BasePlayerService]:
        next_player: Optional[BasePlayerService] = None

        self._turn_index += 1

        player_turn_order: List[BasePlayerService] = self._create_player_turn_order()
        if any(player_turn_order):
            self._player_turn_order = player_turn_order
            next_player, unused_is_final_turn = self._get_next_player_in_turn()

            new_card: BaseCard = self._levelled_card_service.get_next_card_to_reveal(self._round_index, self._cards_to_reveal)
            new_card.reveal_card(self._cards)

            self._harvest_type_for_round = self._harvest_types_by_round[self._turn_index]
        else:
            are_any_more_rounds: bool = self._increment_round_index()
            if are_any_more_rounds:
                self._player_turn_order = self._create_player_turn_order()
                next_player, unused_is_final_turn = self._get_next_player_in_turn()
        return next_player

    def _increment_round_index(self) -> bool:
        if self._round_index == game_constants.number_of_rounds:
            return False

        self._round_index += 1
        self._turn_index = 0
        self._harvest_type_for_round = self._harvest_types_by_round[self._round_index]

        print(f"Round {self._round_index}, Harvest Type: {self._harvest_type_for_round.name}")

        for card in self._cards:
            if isinstance(card, BaseResourceContainingCard):
                card.refill_action()

        for player in self._players:
            for dwarf in player.dwarves:
                dwarf.clear_active_card()

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
