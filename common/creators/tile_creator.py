from typing import List
from buisness_logic.tiles import *
from core.baseClasses.base_tile import BaseTile

class TileCreator(object):
    
    def create_all_tiles(self) -> List[BaseTile]:
        """Returns a list containing a single instance of all of the tiles"""
        tiles = [
            animal_storage_tiles.CuddleRoomTile(,,
            animal_storage_tiles.BreakfastRoomTile(,,
            animal_storage_tiles.StubbleRoomTile(,,
            conversion_tiles.TraderTile(,,
            conversion_tiles.SlaughteringCaveTile(,,
            conversion_tiles.CookingCaveTile(,,
            conversion_tiles.PeacefulCaveTile(,,
            conversion_tiles.HuntingParlorTile(,,
            conversion_tiles.BeerParlorTile(,,
            conversion_tiles.BlacksmithingPalorTile(,,
            conversion_tiles.SparePartStorageTile(,,
            dwelling.Dwelling(,,
            dwelling.SimpleStoneDwelling(,,
            dwelling.SimpleWoodDwelling(,,
            dwelling.MixedDwelling(,,
            dwelling.CoupleDwelling(,,
            dwelling.AdditionalDwelling(,,
            game_change_tiles.WorkRoomTile(,,
            game_change_tiles.GuestRoomTile(,,
            game_change_tiles.OfficeRoomTile(,,
            point_tiles.WeavingParlorTile(,,
            point_tiles.MilkingParlorTile(,,
            point_tiles.StateParlorTile(,,
            point_tiles.StoneStorageTile(,,
            point_tiles.OreStorageTile(,,
            point_tiles.MainStorageTile(,,
            point_tiles.WeaponStorageTile(,,
            point_tiles.SuppliesStorageTile(,,
            point_tiles.BroomChamberTile(,,
            point_tiles.TreasureChamberTile(,,
            point_tiles.FoodChamberTile(,,
            point_tiles.PrayerChamberTile(,,
            point_tiles.WritingChamberTile(,,
            point_tiles.FodderChamberTile(,,
            purchase_tiles.CarpenterTile(,,
            purchase_tiles.StoneCarverTile(,,
            purchase_tiles.BlacksmithTile(,,
            purchase_tiles.BuilderTile(,,
            resource_tiles.MinerTile(,,
            resource_tiles.WoodSupplierTile(,,
            resource_tiles.StoneSupplierTile(,,
            resource_tiles.RubySupplierTile(,
            ]
        return tiles