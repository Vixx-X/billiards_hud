import enum

RADIUS = 5
class BallColor(enum.Enum):
    ERROR = 0
    RED = 1
    YELLOW = 2
    WHITE = 3

    def get_BGR(self):
        if self == self.RED:
            return (0, 0, 255)
        if self == self.YELLOW:
            return (0, 255, 255)
        if self == self.WHITE:
            return (255, 255, 255)
        return (0, 0, 0)

def angle_diff(angle1, angle2):
    rest = abs(angle2 - angle1)
    return min(rest, 255 - rest)

def is_red(hsv_color):
    return hsv_color[0] > 160
    # return angle_diff(hsv_color[0], 255) <= 20

def is_yellow(hsv_color):
    return 30 > hsv_color[0] > 5
    # return angle_diff(hsv_color[0], 55) <= 13

def is_white(hsv_color):
    return hsv_color[1] < 100
    # return hsv_color[0] < 20 and hsv_color[1] < 20 and hsv_color[2] > 240

def classify_color(color):
    if is_white(color):
        return BallColor.WHITE
    elif is_red(color):
        return BallColor.RED
    elif is_yellow(color):
        return BallColor.YELLOW
    return BallColor.ERROR

class Ball:
    x = 0
    y = 0
    r = RADIUS
    color = BallColor.ERROR
    velocity = 0

    def __init__(self, x, y, color=None) -> None:
        self.x = x
        self.y = y
        self.color = color

    def set_color(self, color):
        self.color = classify_color(color)

    def is_intercepting(self, ball):
        (x1, y1), (x2, y2) = (self.x, self.y), (ball.x, ball.y)
        return (x2 - x1)**2 + (y2 - y1)**2 <= (self.r + ball.r)**2

    def is_overlapping(self, ball):
        (x1, y1), (x2, y2) = (self.x, self.y), (ball.x, ball.y)
        return (x2 - x1)**2 + (y2 - y1)**2 <= ((self.r + ball.r)/2)**2
