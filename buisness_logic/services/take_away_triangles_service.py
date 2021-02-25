from typing import Tuple, List


class TakeAwayTrianglesService(object):
    tolerance: int = 0.001

    def calculate_next(self, n1: float, n2: float, n3: float) -> Tuple[float, float, float]:
        m1: float = abs(n1 - n2)
        m2: float = abs(n2 - n3)
        m3: float = abs(n3 - n1)
        return m1, m2, m3

    def normalise(self, n1: float, n2: float, n3: float) -> Tuple[float, float, float]:
        numbers_as_list: list = [n1, n2, n3]
        numbers_as_list = sorted(numbers_as_list)
        m_centre: float = numbers_as_list[1]
        numbers_as_list = [a - m_centre for a in numbers_as_list]
        return tuple(numbers_as_list)

    def iterate_through(
            self,
            n1: float,
            n2: float,
            n3: float,
            iterations: int = 200,
            normalise: bool = False) -> List[Tuple[float, float, float]]:
        visited: List[Tuple[float, float, float]] = []
        last_visited: Tuple[float, float, float] = (n1, n2, n3) if not normalise else self.normalise(n1, n2, n3)
        while len(visited) < iterations and not self.has_previously_visited(last_visited, visited):
            visited.append(last_visited)
            next_visited: Tuple[float, float, float] = self.calculate_next(last_visited[0], last_visited[1], last_visited[2])
            last_visited = next_visited
        return visited

    def has_previously_visited(self, last_visited: Tuple[float, float, float], visited: List[Tuple[float, float, float]]) -> bool:
        has_visited: bool = False
        for tri in visited:
            within_index_0 = abs(last_visited[0] - tri[0]) < self.tolerance
            within_index_1 = abs(last_visited[1] - tri[1]) < self.tolerance
            within_index_2 = abs(last_visited[2] - tri[2]) < self.tolerance
            has_visited = within_index_0 and within_index_1 and within_index_2
            if has_visited:
                break
        return has_visited
