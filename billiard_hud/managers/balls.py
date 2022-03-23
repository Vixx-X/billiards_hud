import cv2
import numpy as np
from objects.balls import BallColor
from managers.table import manager as TableManager


class BallManager:
    red_positions = []
    yellow_positions = []
    white_positions = []
    show_tracelines = False

    speed_accums = {
        BallColor.WHITE: 0,
        BallColor.RED: 0,
        BallColor.YELLOW: 0,
    }

    speed_min = {
        BallColor.WHITE: 0,
        BallColor.RED: 0,
        BallColor.YELLOW: 0,
    }

    speed_max = {
        BallColor.WHITE: 0,
        BallColor.RED: 0,
        BallColor.YELLOW: 0,
    }

    def clear(self):
        self.red_positions = []
        self.yellow_positions = []
        self.white_positions = []

    def get_speeds(self, color):
        hist = max(len(self.get_positions_by_color(color)), 1)
        s_avg = self.speed_accums[color] / hist
        s_max = self.speed_max[color]
        s_min = self.speed_min[color]
        return s_avg, s_min, s_max

    def get_positions_by_color(self, color):
        if color == BallColor.WHITE:
            return self.white_positions
        elif color == BallColor.RED:
            return self.red_positions
        elif color == BallColor.YELLOW:
            return self.yellow_positions
        raise Exception("Unknown color")

    def push(self, ball):
        hist = self.get_positions_by_color(ball.color)
        if len(hist):
            ball2 = hist[-1]
            dist_p = np.sqrt((ball2.x - ball.x) ** 2 + (ball2.y - ball.y) ** 2)
            if not (dist_p < ball.r / 3 or dist_p > 4 * ball.r):
                dist = (224 * 2 + 112 * 2) * dist_p / TableManager.length
                time = (ball.frame - ball2.frame) / 25
                ball.velocity = dist / time
        self.speed_accums[ball.color] += ball.velocity
        self.speed_max[ball.color] = max(ball.velocity, self.speed_max[ball.color])
        self.speed_min[ball.color] = min(ball.velocity, self.speed_min[ball.color])
        hist.append(ball)

    def get_ball_by_color(self, color):
        return self.get_positions_by_color(color)[-1]

    def draw(self, img):
        balls = [self.red_positions, self.white_positions, self.yellow_positions]
        for ball_pos in balls:
            if len(ball_pos):
                ball = ball_pos[-1]
                cv2.circle(
                    img,
                    (ball.x, ball.y),
                    ball.r,
                    ball.color.get_BGR()[::-1],
                    -1,
                )
            if self.show_tracelines:
                for i in range(len(ball_pos) -1):
                    a, b = ball_pos[i], ball_pos[i+1]
                    cv2.line(
                        img,
                        (a.x,a.y),
                        (b.x, b.y),
                        a.color.get_BGR()[::-1],
                        3,
                    )



manager = BallManager()
