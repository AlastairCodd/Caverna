from automated_tests.business_logic_tests.action_tests.place_a_tile_action_tests.given_a_place_a_tile_action import Given_A_PlaceATileAction
from buisness_logic.actions.placeATileAction import PlaceATileAction
from core.enums.caverna_enums import TileTypeEnum, ResourceTypeEnum


class test_when_tile_is_not_specific_but_cost_is_overridden(Given_A_PlaceATileAction):
    def initialise_invalid_sut(self) -> None:
        self.SUT = PlaceATileAction(
            TileTypeEnum.furnishedCavern,
            override_cost={ResourceTypeEnum.stone: 1})

    def test_then_a_value_error_should_be_raise(self) -> None:
        self.assertRaises(ValueError, self.initialise_invalid_sut())
