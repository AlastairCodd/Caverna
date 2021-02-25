from automated_tests.common_tests.entity_tests.point_lookup_tests.given_a_point_lookup import Given_A_PointLookup
from common.entities.point_lookup import PointLookup


class test_when_summed(Given_A_PointLookup):
    def because(self) -> None:
        a: PointLookup = PointLookup(3)
        b: PointLookup = PointLookup(negative_points=2)
        c: PointLookup = PointLookup(negative_offset=3)
        # self._result: PointLookup = sum([a,b,c])
        self._result: PointLookup = a + b + c
        self._expected: int = 3

    def test_then_result_should_be_expected(self) -> None:
        self.assertEqual(abs(self._result), self._expected)