from managers.balls import manager as BallManager
import imgui

def entity_panel():
    imgui.begin("Entities")

    # imgui.text_wrapped(
    #     "This text should automatically wrap on the edge of the window. The current implementation for text wrapping follows simple rules suitable for English and possibly other languages."
    # )

    # if imgui.tree_node("Balls"):
    #     for name, time in Debug.get_times().items():
    #         imgui.label_text(name, f"{time*1000} ms")
    #     imgui.tree_pop()

    imgui.spacing()
    imgui.text("Balls")

    imgui.spacing()
    imgui.text("Red")

    imgui.spacing()
    imgui.text("White")

    imgui.spacing()
    imgui.text("Yellow")

    imgui.separator()

    imgui.spacing()

    imgui.end()
