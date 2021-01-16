from automated_tests.business_logic_tests.validator_tests.partition_resource_validator_tests.given_a_partition_resource_validator import \
    Given_A_PartitionResourceValidator


class Test_When_Resource_Layout_Is_Null(Given_A_PartitionResourceValidator):
    def test_Then_A_ValueError_Should_Be_Thrown(self):
        self.assertRaises(ValueError, self.SUT.does_partition_store_all_resources, None, {}, {})
