import enum

import cv2


def get_area(points):
    return (points[1][0] - points[0][0]) * (points[1][1] - points[1][0])

class TableSide(enum.Enum):
    ERROR = 0
    TOP = 1
    RIGTH = 2
    DOWN = 3
    LEFT = 4


class TableManager:
    points = []
    contour = []
    fake_perspective = False

    def set(self, points):
        p_points = [[float("inf"), float("inf")], [0, 0]]
        points = [p[0] for p in points]
        for x, y in points:
            if p_points[0][0] > x:
                p_points[0][0] = x
            if p_points[1][0] < x:
                p_points[1][0] = x
            if p_points[0][1] > y:
                p_points[0][1] = y
            if p_points[1][1] < y:
                p_points[1][1] = y

        if len(self.points) == 0 or get_area(points) < get_area(p_points):
            self.contour = points
            self.points = p_points

    def collision(self, side, ball):
        if side == TableSide.TOP:
            return ball.y - self.points[0][1] < ball.r
        if side == TableSide.RIGTH:
            return self.points[1][0] - ball.x < ball.r
        if side == TableSide.DOWN:
            return self.points[1][1] - ball.y < ball.r
        if side == TableSide.LEFT:
            return ball.x - self.points[0][0] < ball.r
        return False

    def get_points(self):
        if len(self.contour) == 4:
            return self.contour
        return [
            [self.points[0][0], self.points[0][1]],
            [self.points[1][0], self.points[0][1]],
            [self.points[0][0], self.points[1][1]],
            [self.points[1][0], self.points[1][1]],
        ]

    def draw(self, img):
        if self.fake_perspective:
            cv2.drawContours(img, [self.get_points()], -1, (125, 125, 0), 3)
        else:
            cv2.drawContours(img, [self.contour], -1, (125, 125, 0), 3)


manager = TableManager()
