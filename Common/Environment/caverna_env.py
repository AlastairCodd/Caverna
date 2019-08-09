from typing import Tuple, Dict, List
from gym import Env
from numpy import array, concatenate
from common.creators.card_creator import CardCreator
from common.defaults.players_default import PlayersDefault
from common.entities.dwarf import Dwarf
from common.entities.player import Player
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

        self._players: List[Player] = []
        self._turn_index: int = 0
        self._turn_phase = None
        self._current_player: Player = self._players[0]
        self._starting_player: Player = self._players[0]
        self._cards: List[BaseCard] = []
        self._active_cards: List[BaseCard] = []

        self._point_calculation_service = PointCalculationService()
    
    def reset(self) -> array:
        """Resets the environment
        
        Returns: the observation of the game state"""
        self._players: List[Player] = self._players_default.assign([])
        self._turn_index: int = 0
        self._turn_phase = None
        self._current_player: Player = self._players[0]
        
        card_creator = CardCreator()
        self._cards = card_creator.create_all_cards()
        self._active_cards = [x for x in self._cards if x.level() == -1]
        
        return self.observe()

    def step(self, action) -> Tuple[array, float, bool, Dict]:
        """Takes an action service (either the output of a network or a delayed decision maker)
        and applies the actions to get the next state
        
        Returns:
            array: the observation of the game state
            float: the reward for the last action
            bool: whether or not the game has finished
            dict: additional debug information"""
        if action is None: raise ValueError("action")

        # get dwarf from player

        # filter action to get card
        available_choices = [for c in self._active_cards if c.is_available()]

        player_points: int = self._point_calculation_service.calculate_points(self._current_player)
        return array([]), player_points, False, {}

    def observe(self) -> array:
        observation = array([self._turn_index, self._turn_phase, self._current_player])
        
        return observation

    def _create_player_turn_order(self) -> List[Player]:
        player_dwarf_count: Dict[int, int] = {p.id: 0 for p in self._players}
        player_turn_order: List[Player] = []
        players_with_more_dwarves: List[bool] = [True for p in self._players]
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
    
    def _get_players_starting_at(self, starting_index: int) -> List[Player]:
        result = self._players[starting_index:] + self._players[:starting_index-1]
        return result

    def _observe_player(self, player: Player) -> array:
        player_observation = array(player.get_resources())
        for i in range(self._max_dwarves):
            dwarf = player.dwarves[i] if i <= len(player.dwarves) - 1 else None
            player_observation = concatenate(player_observation, self._observe_dwarf(dwarf), axis=None)

        return player_observation

    def _observe_dwarf(self, dwarf: Dwarf) -> array:
        if dwarf is None: return array([0, 0, 0, 0])
        dwarf_observation = array([dwarf.is_active, dwarf.is_adult, dwarf.weapon.level, dwarf.current_card_id])
        return dwarf_observation