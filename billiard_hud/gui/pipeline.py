import imgui
from managers.pipeline import manager as Pipeline

def pipeline_panel():
    imgui.begin("Pipeline")

    imgui.text("Pipeline Visualization")

    changed, choice = imgui.combo(
        label="Combo",
        current=Pipeline.stages_id.index(Pipeline.selected_stage),
        items=Pipeline.stages_id,
    )

    if changed:
        Pipeline.select_stage(Pipeline.stages_id[choice])

    changed, choice = imgui.checkbox(
        label="Show detections",
        state=Pipeline.show_detections,
    )

    if changed:
        Pipeline.show_detections = choice


    imgui.separator()

    if imgui.tree_node("Pipeline Settings"):
        for stage in Pipeline:
            if imgui.tree_node(stage.id):
                stage.filter_ui()
                imgui.tree_pop()

        imgui.tree_pop()

    imgui.end()
