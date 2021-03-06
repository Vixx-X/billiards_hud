import imgui
from managers.debug import Debug

def debug_panel():
    imgui.begin("Debug Metric")

    imgui.label_text("FPS", f"{int(Debug.get_fps())} ms")

    if imgui.tree_node("Timers"):
        for name, time in Debug.get_times().items():
            imgui.label_text(name, f"{time*1000} ms")
        imgui.tree_pop()

    if imgui.tree_node("Logs"):
        for log in Debug.get_logs():
            imgui.text(log)
        imgui.tree_pop()

    imgui.end()
