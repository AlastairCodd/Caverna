from typing import Dict, cast, Tuple

from automated_tests.business_logic_tests.service_tests.encoder_service_tests.tile_container_encoder_service_tests \
    .given_a_tile_container_encoder_service import Given_A_TileContainerEncoderService
from buisness_logic.effects.allow_farming_effect import AllowFarmingEffect
from buisness_logic.tiles.animal_storage_tiles import BreakfastRoomTile
from buisness_logic.tiles.dwelling import Dwelling, MixedDwelling
from buisness_logic.tiles.game_change_tiles import GuestRoomTile
from buisness_logic.tiles.mine_tiles import CavernTile, TunnelTile, DeepTunnelTile, OreMineTile
from buisness_logic.tiles.outdoor_tiles import FieldTile, MeadowTile, PastureTile
from buisness_logic.tiles.point_tiles import BroomChamberTile, WeavingParlorTile
from common.repositories.simple_player_repository import SimplePlayerRepository
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository


# noinspection PyPep8Naming
class test_when_called(Given_A_TileContainerEncoderService):
    def because(self) -> None:
        self._player = self._initialise_random_player()
        self._result = self.SUT.observe(self._player)

        self._number_of_columns: int = len(self._result) // self._player.tile_count

    def test_then_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_length_should_be_multiple_of_number_of_tiles(self) -> None:
        self.assertTrue(len(self._result) % self._player.tile_count == 0)

    def test_then_same_field_tiles_should_give_same_results(self) -> None:
        tile_19: Tuple[int] = self._result[self._number_of_columns * 19: self._number_of_columns * 20]
        tile_25: Tuple[int] = self._result[self._number_of_columns * 25: self._number_of_columns * 26]
        self.assertTupleEqual(tile_19, tile_25)

    def test_then_same_dwelling_tiles_should_give_same_results(self) -> None:
        tile_28: Tuple[int] = self._result[self._number_of_columns * 28: self._number_of_columns * 29]
        tile_38: Tuple[int] = self._result[self._number_of_columns * 38: self._number_of_columns * 39]
        self.assertTupleEqual(tile_28, tile_38)

    def test_print_result(self) -> None:
        index: int = 0

        for x in self._result:
            if index % self._number_of_columns == 0:
                print()
                print(f"{index // self._number_of_columns:>2}:  ", end="")

            if x == 0:
                print("_, ", end="")
            else:
                print(f"{x:d}, ", end="")
            index += 1

    def _initialise_random_player(self):
        player: BasePlayerRepository = SimplePlayerRepository(0, "player", 0)
        player.give_resources({ResourceTypeEnum.grain: 3, ResourceTypeEnum.veg: 3})

        field_tile_11: FieldTile = FieldTile()
        allow_farming_effect_11: AllowFarmingEffect = cast(AllowFarmingEffect, field_tile_11.effects[0])
        allow_farming_effect_11.plant_resource(player, ResourceTypeEnum.grain)

        field_tile_19: FieldTile = FieldTile()
        allow_farming_effect_19: AllowFarmingEffect = cast(AllowFarmingEffect, field_tile_19.effects[0])
        allow_farming_effect_19.plant_resource(player, ResourceTypeEnum.veg)
        
        field_tile_25: FieldTile = FieldTile()
        allow_farming_effect_25: AllowFarmingEffect = cast(AllowFarmingEffect, field_tile_25.effects[0])
        allow_farming_effect_25.plant_resource(player, ResourceTypeEnum.veg)

        field_tile_34: FieldTile = FieldTile()
        allow_farming_effect_34: AllowFarmingEffect = cast(AllowFarmingEffect, field_tile_34.effects[0])
        allow_farming_effect_34.plant_resource(player, ResourceTypeEnum.grain)
        allow_farming_effect_34.pop_resource(player)

        field_tile_35: FieldTile = FieldTile()
        allow_farming_effect_35: AllowFarmingEffect = cast(AllowFarmingEffect, field_tile_35.effects[0])
        allow_farming_effect_35.plant_resource(player, ResourceTypeEnum.veg)
        allow_farming_effect_35.pop_resource(player)

        tile_and_location: Dict[int, BaseTile] = {
            # 9: None,
            10: MeadowTile(),
            11: field_tile_11,
            12: BreakfastRoomTile(),
            13: BroomChamberTile(),
            # 14: None,

            # 17: None,
            18: MeadowTile(),
            19: field_tile_19,
            20: CavernTile(),
            21: TunnelTile(),
            22: WeavingParlorTile(),

            25: field_tile_25,
            26: MeadowTile(),
            27: PastureTile(),
            28: Dwelling(),
            29: DeepTunnelTile(),
            30: MixedDwelling(),

            # 33: None,
            34: field_tile_34,
            35: field_tile_35,
            # 36: EntryLevelDwelling(),
            37: OreMineTile(),
            38: Dwelling(),
        }

        for location, tile in tile_and_location.items():
            player.tiles[location].set_tile(tile)

        return player
