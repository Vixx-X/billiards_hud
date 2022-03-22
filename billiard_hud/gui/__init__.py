import imgui
from gui.debug_pane import debug_panel
from gui.pipeline import pipeline_panel
from gui.top_menu import top_menu_bar
from gui.video_timeline import video_panel
from managers.debug import Debug

def gui():
    Debug.time("GUI")

    imgui.new_frame()

    top_menu_bar()
    video_panel()
    pipeline_panel()
    imgui.show_test_window()

    Debug.time("GUI")

    debug_panel()
