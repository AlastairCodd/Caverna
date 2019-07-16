from typing import Tuple, Dict
from gym import Env
from numpy import array

class CavernaEnv(Env):
    """Environment for running caverna games"""
    def __init__(self, numberOfPlayers: int = 7):
        """Ctor
        
        Params: numberOfPlayers: int. Must be between 1 and 7 (inclusive)."""
        if numberOfPlayers < 1: raise IndexError("numberOfPlayers")
        if numberOfPlayers > 7: raise IndexError("numberOfPlayers")
        self._numberOfPlayers = numberOfPlayers
    
    def reset(self) -> array:
        raise NotImplementedError()
        
        self._players = []
        
        for x in range(self._numberOfPlayers):
            self._players[x] = player.Player( x, x )
        
    def step(self, action: ActionService) -> Tuple[array, float, bool, Dict]:
        """Takes an action service (either the output of a network or a delayed decision maker)
        and applies the actions to get the next state"""
        if action is None: raise ValueError("action")
        
        
        