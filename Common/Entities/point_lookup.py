class PointLookup(object):
    def __init__(
            self,
            positive_points: int = 0,
            negative_points: int = 0,
            negative_offset: int = 0):
        self.positive_points: int = positive_points
        self.negative_points: int = negative_points
        self.negative_offset: int = negative_offset

    def __abs__(self) -> int:
        points = self.positive_points
        points -= self.negative_points - (min(self.negative_points, self.negative_offset))
        return points

    def __add__(self, other):
        if not isinstance(other, PointLookup):
            raise TypeError("other")
        total_positive_points = self.positive_points + other.positive_points
        total_negative_points = self.negative_points + other.negative_points
        total_negative_offset = self.negative_offset + other.negative_offset
        return PointLookup(total_positive_points, total_negative_points, total_negative_offset)
