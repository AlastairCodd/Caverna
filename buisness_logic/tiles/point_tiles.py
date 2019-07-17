class BaseConditionalPointTile(BaseTile):
    def invoke(self, source: Dict[TileTypeEnum, List[TileTypeEnum]]) -> Dict[TileTypeEnum, List[TileTypeEnum]]:
        raise NotImplementedException("base conditional point effect class")
        
class WeavingParlorTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "Weaving Parlor"
        self._id = 30
        self._isDwelling = False
        self._basePoints = 0
        self._cost = { ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 1 }
        self._effect = [ when purchased receive 1 food per sheep ]
        self._conditionalPoints = { { ResourceTypeEnum.sheep: 1 }: 1 }
        
class MilkingParlorTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "Milking Parlor"
        self._id = 31
        self._isDwelling = False
        self._basePoints = 0
        self._cost = { ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 2 }
        self._effect = [ when purchased receive 1 food per cow ]
        self._conditionalPoints = { { ResourceTypeEnum.cow: 1 }: 1 }
        
class state ParlorTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "State Parlor"
        self._id = 32
        self._isDwelling = False
        self._basePoints = 0
        self._cost = { ResourceTypeEnum.wood: 3, ResourceTypeEnum.coin: 5 }
        self._effect = [ when purchased per adjacent dwelling receive 2 food ]
        self._conditionalPoints = [ 4 per adjacent dwelling ]
        
class StoneStorageTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "Stone Storage"
        self._id = 36
        self._isDwelling = False
        self._basePoints = 0
        self._cost = { ResourceTypeEnum.wood: 3, ResourceTypeEnum.ore: 1 }
        self._effect = [  ]
        self._conditionalPoints = { { ResourceTypeEnum.stone: 1 }: 1 }
        
class OreStorageTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "Ore Storage"
        self._id = 37
        self._isDwelling = False
        self._basePoints = 0
        self._cost = { ResourceTypeEnum.wood: 1, ResourceTypeEnum.ore: 2 }
        self._effect = [  ]
        self._conditionalPoints = { { ResourceTypeEnum.ore: 2 }: 1 }
        
class MainStorageTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "Main Storage"
        self._id = 39
        self._isDwelling = False
        self._basePoints = 0
        self._cost = { ResourceTypeEnum.wood: 2, ResourceTypeEnum.stone: 1 }
        self._effect = [  ]
        self._conditionalPoints = [ 2 per yellow furnishing ]
        
class WeaponStorageTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "Weapon Storage"
        self._id = 40
        self._isDwelling = False
        self._basePoints = 0
        self._cost = { ResourceTypeEnum.wood: 3, ResourceTypeEnum.stone: 2 }
        self._effect = [  ]
        self._conditionalPoints = [ 3 per dwarf with weapon ]
        
class SuppliesStorageTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "Supplies Storage"
        self._id = 41
        self._isDwelling = False
        self._basePoints = 0
        self._cost = { ResourceTypeEnum.food: 3, ResourceTypeEnum.wood: 1 }
        self._effect = [  ]
        self._conditionalPoints = [ 8 if all dwarves have a weapon ]
        
class BroomChamberTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "Broom Chamber"
        self._id = 42
        self._isDwelling = False
        self._basePoints = 0
        self._cost = { ResourceTypeEnum.wood: 1 }
        self._effect = [  ]
        self._conditionalPoints = [ 5 for 5 dwarves and 5 for the 6th dwarf ]
        
class TreasureChamberTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "Treasure Chamber"
        self._id = 43
        self._isDwelling = False
        self._basePoints = 0
        self._cost = { ResourceTypeEnum.wood: 1, ResourceTypeEnum.stone: 1 }
        self._effect = [  ]
        self._conditionalPoints = [ 1 per ruby ]
        
class FoodChamberTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "Food Chamber"
        self._id = 44
        self._isDwelling = False
        self._basePoints = 0
        self._cost = { ResourceTypeEnum.wood: 2, ResourceTypeEnum.vegetable: 2 }
        self._effect = [  ]
        self._conditionalPoints = [ 2 per vegetable and grain ]
        
class PrayerChamberTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "Prayer Chamber"
        self._id = 45
        self._isDwelling = False
        self._basePoints = 0
        self._cost = { ResourceTypeEnum.wood: 2 }
        self._effect = [  ]
        self._conditionalPoints = [ 8 if no dwarves have a weapon ]
        
class WritingChamberTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "Writing Chamber"
        self._id = 46
        self._isDwelling = False
        self._basePoints = 0
        self._cost = { ResourceTypeEnum.stone: 2 }
        self._effect = [  ]
        self._conditionalPoints = [ prevents up to 7 negative points ]

class FodderChamberTile(BaseConditionalPointTile):
    def __init__(self):
        self._name = "Fodder Chamber"
        self._id = 47
        self._isDwelling = False
        self._basePoints = 0
        self._cost = { ResourceTypeEnum.grain: 2, ResourceTypeEnum.stone: 1 }
        self._effect = [  ]
        self._conditionalPoints = [ 1 per 3 farm animals ]