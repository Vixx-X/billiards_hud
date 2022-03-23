import imgui
from managers.media import manager as Media
from managers.table import manager as Table
from managers.pipeline import manager as Pipeline

def video_panel():

    if Media.ready():
        imgui.begin("Video")

        changed, _ = imgui.checkbox(
            label="Play/Stop",
            state=Media.stopped,
        )

        if changed:
            Media.toggle()


        changed, frame = imgui.slider_int(
                  label="current frame",
                  value=Media.frame_id,
                  min_value=Media.start,
                  max_value=Media.end)

        if changed:
            Media.set_frame(frame)


        changed, (start, end) = imgui.drag_int2(
                  label=f"frame range ({Media.start}, {Media.end})",
                  value0=Media.start,
                  value1=Media.end,
                  change_speed=1,
                  min_value=0,
                  max_value=Media.frame_size,
                  format="%d")

        if changed:
            Media.set_start(start)
            Media.set_end(end)


        changed, value = imgui.checkbox(
            label="Show detections",
            state=Pipeline.show_detections,
        )

        if changed:
            Pipeline.show_detections = value

        changed, value = imgui.checkbox(
            label="Warp perspective",
            state=Table.fake_perspective,
        )

        if changed:
            Table.fake_perspective = value

        imgui.end()
