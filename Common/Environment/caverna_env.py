from typing import Tuple, Dict, List
from gym import Env
from numpy import array
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
        self._active_cards = [x for x in self._cards if x.get_level() == -1]
        
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
        any_players_with_dwarves = True
        while any_players_with_dwarves:
            for i in range(self._number_of_players):
                index = i + self._starting_player.id % self._number_of_players
                player_dwarves = self._players[index].dwarves
                if player_dwarves.count() < player_dwarf_count[index]:
                    