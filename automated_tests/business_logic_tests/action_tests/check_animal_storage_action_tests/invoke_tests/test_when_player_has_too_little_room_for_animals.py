from typing import Dict, cast

from automated_tests.business_logic_tests.action_tests.check_animal_storage_action_tests.given_a_check_animal_storage_action import \
    Given_A_CheckAnimalStorageAction
from automated_tests.mocks.mock_player import MockPlayer
from buisness_logic.tiles.mine_tiles import OreMineTile, RubyMineTile
from buisness_logic.tiles.outdoor_tiles import PastureTile
from common.entities.result_lookup import ResultLookup
from common.entities.tile_entity import TileEntity
from core.enums.caverna_enums import ResourceTypeEnum
from core.services.base_player_service import BasePlayerService


class test_when_player_has_too_little_room_for_animals(Given_A_CheckAnimalStorageAction):
    # noinspection PyTypeChecker
    def because(self) -> None:
        self._player: BasePlayerService = self._initialise_player()

        self._result: ResultLookup[int] = self.SUT.invoke(
            self._player,
            None,  # Unused
            None)  # Unused

    def _initialise_player(self) -> MockPlayer:
        starting_resources: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.sheep: 3,
            ResourceTypeEnum.donkey: 3,
            ResourceTypeEnum.cow: 2,
            ResourceTypeEnum.stone: 1
        }

        player: MockPlayer = MockPlayer(resources=starting_resources)

        # _ 1 2 _ | _ _ _ 7
        # 8 x x x | x x x _
        # _ x x x | x x x _
        # _ x x x | C x x _
        # _ x x P | D m m dm
        # _ _ _ _ | _ _ _ _

        outside_pasture_tile_entity: TileEntity = player.tiles[35]
        outside_pasture_tile_entity.set_tile(PastureTile())

        player.tiles[37].set_tile(OreMineTile())
        player.tiles[38].set_tile(OreMineTile())
        player.tiles[39].set_tile(RubyMineTile())

        return player

    def test_then_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_false(self) -> None:
        self.assertFalse(self._result.flag)

    def test_then_result_value_should_be_none(self) -> None:
        self.assertIsNone(self._result.value)

    def test_then_result_errors_should_not_be_empty(self) -> None:
        self.assertGreater(len(cast(list, self._result.errors)), 0)
