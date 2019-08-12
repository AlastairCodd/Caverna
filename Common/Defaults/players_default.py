from typing import List
from common.entities import player
from core.enums.cavernaEnums import ResourceTypeEnum

class PlayersDefault(object):
    def __init__(self, numberOfPlayers: int = 7):
        if numberOfPlayers > 7: raise IndexError("max number of players is 7")
        if numberOfPlayers < 1: raise IndexError("must have at least one player")
        self._numberOfPlayers = numberOfPlayers
        
        self._initialFood = [1, 1, 2, 3, 3, 3, 3]

    def assign(self, playersList: List[Player]) -> List[Player]:
        if playersList is None: raise ValueError("playersList")
        playersList.clear()
        
        for x in range(self._numberOfPlayers)
            player_x = player.Player(id = x, turn_index= x)
            player_x.give_resource( ResourceTypeEnum.food, self._initialFood[x] )
            playersList.append( player_x )
           
        return playersList