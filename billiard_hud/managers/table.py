import enum

import cv2
import numpy as np


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
    length = 0
    fake_perspective = False

    def set(self, contour):
        p_points = [[float("inf"), float("inf")], [0, 0]]
        points = [p[0] for p in contour]
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
            self.contour = contour
            self.points = p_points
            # self.length = 2 * (p_points[1][0] - p_points[0][0]) + 2 * (
            #     p_points[0][1] - p_points[0][0]
            # )
            self.length = cv2.arcLength(contour, True)

    def _collision(self, side, ball):
        if side == TableSide.TOP:
            return ball.y - self.points[0][1] < ball.r * 2
        if side == TableSide.RIGTH:
            return self.points[1][0] - ball.x < ball.r * 2
        if side == TableSide.DOWN:
            return self.points[1][1] - ball.y < ball.r * 2
        if side == TableSide.LEFT:
            return ball.x - self.points[0][0] < ball.r * 2
        return False

    def collision(self, side, ball):
        if self._collision(side, ball):
            return True
        return False

    def get_points(self):
        if len(self.contour) == 4:
            return [[x[0].tolist()] for x in self.contour]
        return [
            [self.points[0][0], self.points[0][1]],
            [self.points[1][0], self.points[0][1]],
            [self.points[0][0], self.points[1][1]],
            [self.points[1][0], self.points[1][1]],
        ]

    def draw(self, img):
        if self.fake_perspective:
            cv2.drawContours(img, np.array([self.get_points()]), -1, (125, 125, 0), 3)
        else:
            cv2.drawContours(img, [self.contour], -1, (125, 125, 0), 3)


manager = TableManager()
