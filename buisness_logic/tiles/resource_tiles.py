from buisness_logic.effects import *
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum


class MinerTile(BaseTile):
    def __init__(self):
        self._name = "Miner"
        self._id = 15
        self._isDwelling = False
        self._basePoints = 3
        self._cost = { ResourceTypeEnum.wood: 1, ResourceTypeEnum.stone: 1 }
        self._effect = [ resource_effects.ReceiveConditional( {ResourceTypeEnum.donkey: 1}, {ResourceTypeEnum.ore: 1} ) ]

class WoodSupplierTile(BaseTile):
    def __init__(self):
        self._name = "Wood Supplier"
        self._id = 18
        self._isDwelling = False
        self._basePoints = 2
        self._cost = { ResourceTypeEnum.stone: 1 }
        self._effect = [ resource_effects.ReceiveForTurns( {ResourceTypeEnum.wood: 1 }, 7 ) ]

class StoneSupplierTile(BaseTile):
    def __init__(self):
        self._name = "Stone Supplier"
        self._id = 19
        self._isDwelling = False
        self._basePoints = 1
        self._cost = { ResourceTypeEnum.wood: 1 }
        self._effect = [ resource_effects.ReceiveForTurns( {ResourceTypeEnum.stone: 1 }, 5 ) ]

class RubySupplierTile(BaseTile):
    def __init__(self):
        self._name = "Ruby Supplier"
        self._id = 20
        self._isDwelling = False
        self._basePoints = 2
        self._cost = { ResourceTypeEnum.stone: 2, ResourceTypeEnum.wood: 2 }
        self._effect = [ resource_effects.ReceiveForTurns( {ResourceTypeEnum.ruby: 1 }, 4 ) ]
