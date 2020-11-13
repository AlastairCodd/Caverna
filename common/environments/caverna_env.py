from typing import Tuple, Dict, List
from gym import Env
from numpy import array, concatenate
from common.forges.card_forge import CardForge
from common.defaults.players_default import PlayersDefault
from common.entities.dwarf import Dwarf
from core.services.base_player_service import BasePlayerService
from common.services.point_calculation_service import PointCalculationService
from core.baseClasses.base_card import BaseCard


class CavernaEnv(Env):
    """Environment for running caverna games"""
    def __init__(self, number_of_players: int = 7):
        """Ctor
        
        Params: numberOfPlayers: int. Must be between 1 and 7 (inclusive)."""
        if number_of_players < 1: raise IndexError("numberOfPlayers")
        if number_of_players > 7: raise IndexError("numberOfPlayers")
        self._number_of_players = number_of_players
        self._players_default = PlayersDefault(self._number_of_players)

        self._players: List[BasePlayerService] = []
        self._turn_index: int = 0
        self._turn_phase = None
        self._current_player: BasePlayerService = self._players[0]
        self._starting_player: BasePlayerService = self._players[0]
        self._cards: List[BaseCard] = []

        self._point_calculation_service = PointCalculationService()
    
    def reset(self) -> array:
        """Resets the environment
        
        Returns: the observation of the game state"""
        self._players: List[BasePlayerService] = self._players_default.assign([])
        self._turn_index: int = 0
        self._turn_phase = None
        self._current_player: BasePlayerService = self._players[0]
        
        card_creator = CardForge()
        self._cards = card_creator.create_all_cards()

        return self.observe()

    def render(self, mode='human'):
        pass

    def step(self, action: array) -> Tuple[array, float, bool, Dict]:
        """Takes an action service (either the output of a network or a delayed decision maker)
        and applies the actions to get the next state
        
        Returns:
            array: the observation of the game state
            float: the reward for the last action
            bool: whether or not the game has finished
            dict: additional debug information"""
        if action is None:
            raise ValueError("action")
        player_points_at_turn_start: int = self._point_calculation_service.calculate_points(self._current_player)



        player_points_after_action: int = self._point_calculation_service.calculate_points(self._current_player)
        reward: int = player_points_after_action - player_points_at_turn_start
        return array([]), reward, False, {}

    def observe(self) -> array:
        observation = array([self._turn_index, self._turn_phase, self._current_player])
        
        return observation

    def _create_player_turn_order(self) -> List[BasePlayerService]:
        player_dwarf_count: Dict[int, int] = {p.id: 0 for p in self._players}
        player_turn_order: List[BasePlayerService] = []
        players_with_more_dwarves: List[bool] = [True for _ in self._players]
        while any(players_with_more_dwarves):
            # for each player, starting at starting player
            for current_player in self._get_players_starting_at(self._starting_player.id):

                # does the current player have more dwarves than currently stored
                if len(current_player.dwarves) < player_dwarf_count[current_player.id]:
                    player_turn_order.append( current_player )

                    player_dwarf_count[current_player.id] += 1

                if len(current_player.dwarves) < player_dwarf_count[current_player.id]:
                    players_with_more_dwarves[current_player.id] = False

        return player_turn_order
    
    def _get_players_starting_at(self, starting_index: int) -> List[BasePlayerService]:
        result = self._players[starting_index:] + self._players[:starting_index-1]
        return result

    def _observe_player(self, player: BasePlayerService) -> array:
        player_observation = array(player.resources)
        for i in range(6):
            dwarf = player.dwarves[i] if i <= len(player.dwarves) - 1 else None
            player_observation = concatenate(player_observation, self._observe_dwarf(dwarf), axis=None)

        return player_observation

    def _observe_dwarf(self, dwarf: Dwarf) -> array:
        if dwarf is None: return array([0, 0, 0, 0])
        dwarf_observation = array([dwarf.is_active, dwarf.is_adult, dwarf.weapon.level, dwarf.current_card_id])
        return dwarf_observation