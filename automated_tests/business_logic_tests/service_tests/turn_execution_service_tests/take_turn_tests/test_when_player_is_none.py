from automated_tests.business_logic_tests.service_tests.turn_execution_service_tests.given_a_turn_execution_service import Given_A_TurnExecutionService
from automated_tests.mocks.mock_card import MockCard
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.enums.harvest_type_enum import HarvestTypeEnum


class Test_When_player_Is_Null(Given_A_TurnExecutionService):
    def because(self) -> None:
        self._turn_descriptor: TurnDescriptorLookup = TurnDescriptorLookup(
            [MockCard()],
            [],
            0,
            0,
            HarvestTypeEnum.NoHarvest
        )

    def test_Then_A_ValueError_Should_Be_Thrown(self):
        self.assertRaises(ValueError, self.SUT.get_turn, None, self._turn_descriptor)
