from automated_tests.business_logic_tests.effects_tests.resource_effects_tests.receive_proportional_on_purchase_effect_tests\
    .given_a_ReceiveProportionalOnPurchaseEffect import Given_A_ReceiveProportionalOnPurchaseEffect


class Test_When_Player_Is_Null(Given_A_ReceiveProportionalOnPurchaseEffect):
    def test_Then_A_ValueError_Should_Be_Thrown(self):
        self.assertRaises(ValueError, self.SUT.invoke, None)
