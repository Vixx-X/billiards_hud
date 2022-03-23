import enum

import cv2
from cv2 import arcLength
import numpy as np


class StickManager:
    points = []
    length = 0

    def set(self, points):
        self.points[0][0] = points[0]
        self.points[0][1] = points[1]
        self.points[1][0] = points[2]
        self.points[1][1] = points[3]

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

    def draw(self, img):
        if self.fake_perspective:
            points = [[x.tolist()] for x in self.get_points()]
            cv2.drawContours(img, np.array([points]), -1, (125, 125, 0), 3)
        else:
            cv2.drawContours(img, [self.contour], -1, (125, 125, 0), 3)


manager = StickManager()
