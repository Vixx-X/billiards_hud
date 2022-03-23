from objects.balls import BallColor


class BallManager:
    red_positions = []
    yellow_positions = []
    white_positions = []

    red_collisions = []
    yellow_collisions = []
    white_collisions = []

    def get_collisions_by_color(self, color):
        if color == BallColor.WHITE:
            return self.white_collisions
        elif color == BallColor.RED:
            return self.red_collisions
        elif color == BallColor.YELLOW:
            return self.white_collisions
        raise Exception("Unknown color")

    def get_positions_by_color(self, color):
        if color == BallColor.WHITE:
            return self.white_positions
        elif color == BallColor.RED:
            return self.red_positions
        elif color == BallColor.YELLOW:
            return self.white_positions
        raise Exception("Unknown color")

    def push(self, ball):
        self.get_positions_by_color(ball.color).append(ball)

    def get_ball_by_color(self, color):
        return self.get_positions_by_color(color)[-1]




manager = BallManager()
