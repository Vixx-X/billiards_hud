import imgui
from managers.pipeline import manager as Pipeline

def pipeline_panel():
    imgui.begin("Pipeline")

    imgui.text("Pipeline settings for visualization")

    for stage in Pipeline:
        if imgui.tree_node(stage.id):
            stage.filter_ui()
            imgui.tree_pop()

    imgui.end()
