from typing import Dict, List
from math import floor


def partitions(index: int) -> int:
    if index < 0:
        raise ValueError(f"Index must be positive {index}")
    if index == 0:
        return 1

    summations_for_index: Dict[int, bool] = summations(index)
    result: int = 0
    for term_in_summation in summations_for_index:
        term_in_partition: int = partitions(index - term_in_summation)
        if summations_for_index[term_in_summation]:
            result += term_in_partition
        else:
            result -= term_in_partition

    return result


def summations(index: int) -> Dict[int, bool]:
    positions_for_index: List[int] = positions(index)
    result: Dict[int, bool] = {}
    for i in range(len(positions_for_index)):
        term_in_position: int = positions_for_index[i]
        add: bool = floor(i / 2) % 2 == 0
        result[term_in_position] = add

    return result


def positions(index: int) -> List[int]:
    sequence_for_index: List[int] = sequence(index)
    next_term: int = 1
    result: List[int] = [1]
    for term_in_sequence in sequence_for_index:
        next_term += term_in_sequence
        if next_term < index:
            result.append(next_term)
        else:
            break

    return result


def sequence(index: int) -> List[int]:
    result: List[int] = []

    for i in range(1, index):
        # 1 2 3 4 5 6 
        # 1 3 2 5 3 7 ...
        next_term: int
        if i % 2 == 0:  # even
            next_term = i + 1
        else:  # odd
            next_term = int((i + 1) / 2)
        result.append(next_term)

    return result


if __name__ == "__main__":
    b = sequence(12)
    for i in b:
        print(i)

    print("")
    c = positions(12)
    for i in c:
        print(i)

    print("")
    d = summations(12)
    for i in d:
        add: str = "+" if d[i] else "-"
        print(f"{i} {add}")

    partitions(2)
    print("")
    for i in range(12):
        e = partitions(i)
        print(e)
