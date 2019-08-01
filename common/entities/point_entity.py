class PointEntity(object):
    def __init__(self,
                 positive_points: int = 0,
                 negative_points: int = 0,
                 negative_offset: int = 0):
        self.positive_points: int = positive_points
        self.negative_points: int = negative_points
        self.negative_offset: int = negative_offset

    def get_points(self) -> int:
        points = self.positive_points
        points -= self.negative_points - (min(self.negative_points, self.negative_offset))
        return points
