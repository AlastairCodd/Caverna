from typing import Generator, List, Union


class IntegerPartitionForge:
    def generate_integer_partitions(self, integer: int, max_value: Union[int, None] = None) -> Generator[List[int], None, None]:
        """Generate the partitions of an integer

        :param integer: The integer. This must be greater than zero.
        :param max_value: The maximum value of the remaining values. If this is null, this defaults to the integer.
        This must be greater than or equal to zero.
        """
        if integer < 0:
            raise ValueError(f"integer {integer} must be greater than zero")
        if max_value is None:
            max_value = integer
        if max_value < 0:
            raise ValueError(f"max_value {max_value} must be greater than or equal to 0")
        if integer == 0:
            yield []

        for i in range(min(integer, max_value), 0, -1):
            for remaining_partition in self.generate_integer_partitions(integer - i, i):
                result: List[int] = [i] + remaining_partition
                yield result
