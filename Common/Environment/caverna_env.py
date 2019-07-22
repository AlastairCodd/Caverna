from typing import Tuple, Dict
from gym import Env
from numpy import array
from common.creators.card_creator import CardCreator
from common.defaults.players_default import PlayersDefault
from common.entities import player

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
        """Resets the environment
        
        Returns: the observation of the game state"""
        self._players = self._playersDefault.assign( [] )
        self._turnIndex = 0
        self._turnPhase = raise ValueError()
        self._currentPlayer = 0
        
        cardCreator = CardCreator()
        self._cards = cardCreator.create_all_cards()
        self._activeCards = [x for x in self._cards if x.get_level() == -1]
        
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
        # filter action to get card
        cardChoice = None
        
        
    def observe(self):
        observation = array([self._turnIndex, self._turnPhase, self._currentPlayer])
        
        return observation