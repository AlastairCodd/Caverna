from automated_tests.business_logic_tests.effects_tests.resource_effects_tests.allow_farming_effect_tests.given_an_allow_farming_effect import \
    Given_An_AllowFarmingEffect
from automated_tests.mocks.mock_player import MockPlayer
from core.enums.caverna_enums import ResourceTypeEnum


class Test_When_ResourceType_Is_Null(Given_An_AllowFarmingEffect):
    def test_Then_A_ValueError_Should_Be_Thrown(self):
        self.assertRaises(ValueError, self.SUT.plant_resource, MockPlayer(), ResourceTypeEnum.wood)
