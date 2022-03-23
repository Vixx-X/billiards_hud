import cv2
from objects.balls import BallColor

class BallManager:
    red_positions = []
    yellow_positions = []
    white_positions = []

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
        self.get_positions_by_color(ball.color).append(ball)

    def get_ball_by_color(self, color):
        return self.get_positions_by_color(color)[-1]

    def draw(self, img):
        balls = [self.red_positions, self.white_positions, self.yellow_positions]
        for ball_pos in balls:
            if len(ball_pos):
                ball = ball_pos[-1]
                cv2.circle(
                    img, (ball.x, ball.y), ball.r,
                    ball.color.get_BGR()[::-1], -1,
                )


manager = BallManager()
