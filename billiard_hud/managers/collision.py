from managers.media import manager as MediaManager
from managers.balls import manager as Balls
from managers.stick import manager as Stick
from managers.table import TableSide, manager as Table
from objects.balls import BallColor

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

    def get_ball_color_by_name(self, name):
        ma = {
            "Red Ball" : BallColor.RED,
            "White Ball" : BallColor.WHITE,
            "Yellow Ball": BallColor.YELLOW,
        }
        return ma[name]

    def get_wall_side_by_name(self, name):
        ma = {
            "Top Wall": TableSide.TOP,
            "Rigth Wall" : TableSide.RIGTH,
            "Down Wall": TableSide.DOWN,
            "Left Wall": TableSide.LEFT,
        }
        return ma[name]

    before_state = dict()

    def run(self):
        frame = MediaManager.frame_id
        for idx, ball in enumerate(BALLS):
            b1 = Balls.get_ball_by_color(self.get_ball_color_by_name(ball))
            for ball2 in BALLS[idx+1:]:
                b2 = Balls.get_ball_by_color(self.get_ball_color_by_name(ball2))
                rel_name = f"{ball}_{ball2}"
                before = self.before_state.get(rel_name, False)
                if b1.is_intercepting(b2):
                    if not before:
                        self.data["Balls"][ball][ball2] += 1
                        self.data["Balls"][ball2][ball] += 1
                        self.before_state[rel_name] = True
                        msg = f"[{frame}] {ball} colide with {ball2}"
                        msg = f"[{frame}] {ball2} colide with {ball}"
                        self.logs.append(msg)
                else:
                    self.before_state[rel_name] = False

            rel_name = f"{ball}_Stick"
            before = self.before_state.get(rel_name, False)
            if Stick.collision(b1):
                if not before:
                    self.data["Balls"][ball]["Stick"] += 1
                    self.data["Stick"][ball] += 1
                    self.before_state[rel_name] = True
                    msg = f"[{frame}] Stick strike {ball}"
                    self.logs.append(msg)

                    Balls.clear()
                    # clear positions on Balls
            else:
                self.before_state[rel_name] = False

            for wall in WALLS:
                side = self.get_wall_side_by_name(wall)
                rel_name = f"{ball}_{wall}"
                before = self.before_state.get(rel_name, False)
                if Table.collision(side, b1):
                    if not before:
                        self.data["Balls"][ball][wall] += 1
                        self.data["Walls"][wall][ball] += 1
                        self.before_state[rel_name] = True
                        msg = f"[{frame}] {ball} colide with {wall}"
                        self.logs.append(msg)
                else:
                    self.before_state[rel_name] = False


manager = CollisionManager()
