from automated_tests.business_logic_tests.action_tests.place_a_single_tile_action_tests.given_a_place_a_single_tile_action import Given_A_PlaceASingleTileAction
from buisness_logic.actions.place_a_single_tile_action import PlaceASingleTileAction
from core.enums.caverna_enums import TileTypeEnum, ResourceTypeEnum


class test_when_tile_is_not_specific_but_cost_is_overridden(Given_A_PlaceASingleTileAction):
    def initialise_invalid_sut(self) -> None:
        self.SUT = PlaceASingleTileAction(
            TileTypeEnum.furnishedCavern,
            override_cost={ResourceTypeEnum.stone: 1})

    def test_then_a_value_error_should_be_raised(self) -> None:
        self.assertRaises(ValueError, self.initialise_invalid_sut)
