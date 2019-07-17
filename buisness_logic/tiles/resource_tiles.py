from buisness_logic.effects import *

class MinerTile(BaseTile):
    def __init__(self):
        self._name = "Miner"
        self._id = 15
        self._isDwelling = False
        self._basePoints = 3
        self._cost = { ResourceTypeEnum.wood: 1, ResourceTypeEnum.stone: 1 }
        self._effect = [ resourceEffects.ReceiveConditional( {ResourceTypeEnum.donkey: 1}, {ResourceTypeEnum.ore: 1} ) ]
