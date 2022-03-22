import imgui
from managers.debug import Debug

def debug_panel():
    imgui.begin("Debug Metric")

    imgui.label_text("FPS", f"{int(Debug.get_fps())}")

    if imgui.tree_node("Timers"):
        for name, time in Debug.get_times().items():
            imgui.label_text(name, f"{time*1000} ms")
        imgui.tree_pop()

    if imgui.tree_node("Texts"):
        for name, text in Debug.get_texts().items():
            imgui.label_text(name, text)
        imgui.tree_pop()

    if imgui.tree_node("Logs"):
        for log in Debug.get_logs():
            imgui.text(log)
        imgui.tree_pop()


    changed, value = imgui.slider_int(
              label="down/up sampling",
              value=Debug.scale_factor,
              min_value=1,
              max_value=10)

    if changed:
        Debug.scale_factor = value


    imgui.end()
