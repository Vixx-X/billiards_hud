from managers.balls import manager as BallManager
from managers.collision import manager as CollisionManager
import imgui

from objects.balls import BallColor

def stick_part():
    imgui.text("Stick")
    for ball in CollisionManager.BALLS:
        imgui.label_text(ball, str(CollisionManager.data["Stick"][ball]))


name2color = {
    CollisionManager.BALLS[0] : BallColor.RED,
    CollisionManager.BALLS[1] : BallColor.WHITE,
    CollisionManager.BALLS[2] : BallColor.YELLOW,
}

def ball_part():
    imgui.text("Balls")
    for ball in CollisionManager.BALLS:
        if imgui.tree_node(ball):
            color = name2color[ball]
            speeds = BallManager.get_speeds(color)
            imgui.label_text("AVG", str(speeds[0]))
            imgui.label_text("MIN", str(speeds[1]))
            imgui.label_text("MAX", str(speeds[2]))
            for name, values in CollisionManager.data["Balls"][ball].items():
                imgui.label_text(name, str(values))
            imgui.tree_pop()

def wall_part():
    imgui.text("Walls")
    for wall in CollisionManager.WALLS:
        if imgui.tree_node(wall):
            for name, values in CollisionManager.data["Walls"][wall].items():
                imgui.label_text(name, str(values))
            imgui.tree_pop()


def log_part():
    imgui.text("Events")

    imgui.spacing()
    for log in CollisionManager.logs:
        imgui.text_wrapped(log)

def entity_panel():
    imgui.begin("Entities Collisions and Events")

    stick_part()
    imgui.separator()
    ball_part()
    imgui.separator()
    wall_part()
    imgui.separator()
    log_part()

    imgui.end()
