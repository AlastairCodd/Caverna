from typing import Tuple, Dict
from gym import Env
from numpy import array
from common.entities import player
from common.defaults.players_default import PlayersDefault

class CavernaEnv(Env):
    """Environment for running caverna games"""
    def __init__(self, numberOfPlayers: int = 7):
        """Ctor
        
        Params: numberOfPlayers: int. Must be between 1 and 7 (inclusive)."""
        if numberOfPlayers < 1: raise IndexError("numberOfPlayers")
        if numberOfPlayers > 7: raise IndexError("numberOfPlayers")
        self._numberOfPlayers = numberOfPlayers
        self._playersDefault = PlayersDefault( self._numberOfPlayers )
    
    def reset(self) -> array:
        self._players = self._playersDefault.assign( [] )
        self._turnIndex = 0
        self._turnPhase = raise ValueError()
        self._currentPlayer = 0

    def step(self, action) -> Tuple[array, float, bool, Dict]:
        """Takes an action service (either the output of a network or a delayed decision maker)
        and applies the actions to get the next state"""
        if action is None: raise ValueError("action")
        
        