from automated_tests.business_logic_tests.effects_tests.resource_effects_tests.receive_proportional_on_purchase_effect_tests.given_a_ReceiveProportionalOnPurchaseEffect import \
    Given_A_ReceiveProportionalOnPurchaseEffect
from buisness_logic.effects.resource_effects import ReceiveProportionalOnPurchaseEffect


class Test_When_Parameters_Are_Null(Given_A_ReceiveProportionalOnPurchaseEffect):
    def test_Then_When_Receive_Is_Null_A_ValueError_Should_Be_Thrown(self):
        self.assertRaises(ValueError, lambda: ReceiveProportionalOnPurchaseEffect(None, {}))

    def test_then_when_SubstituteWith_is_null_a_ValueError_Should_Be_Throw(self) -> None:
        self.assertRaises(ValueError, lambda: ReceiveProportionalOnPurchaseEffect({}, None))
