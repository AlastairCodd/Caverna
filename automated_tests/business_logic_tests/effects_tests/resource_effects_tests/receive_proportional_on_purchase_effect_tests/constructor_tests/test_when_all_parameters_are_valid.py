from automated_tests.business_logic_tests.effects_tests.resource_effects_tests.receive_proportional_on_purchase_effect_tests.given_a_ReceiveProportionalOnPurchaseEffect import \
    Given_A_ReceiveProportionalOnPurchaseEffect


class Test_When_all_parameters_are_valid(Given_A_ReceiveProportionalOnPurchaseEffect):
    def test_then_sut_should_not_be_null(self) -> None:
        self.assertIsNotNone(self.SUT)
