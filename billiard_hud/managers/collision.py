from managers.media import manager as MediaManager

BALLS = [
    "Red Ball",
    "White Ball",
    "Yellow Ball",
]
WALLS = [
    "Top Wall",
    "Rigth Wall",
    "Down Wall",
    "Left Wall",
]
class CollisionManager:
    BALLS = BALLS
    WALLS = WALLS
    logs = []
    data = {
        "Balls": {
            ball: {
                "Stick": 0,
                **{
                    wall:0 for wall in WALLS
                },
                **{
                    balli:0 for balli in BALLS if balli != ball
                },
            }
            for ball in BALLS
        },
        "Stick": {
            ball:0 for ball in BALLS
        },
        "Walls": {
            wall: {
                ball:0 for ball in BALLS
            }
            for wall in WALLS
        },
    }

    last_play = 0

    def run(self):
        pass

manager = CollisionManager()
