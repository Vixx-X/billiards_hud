import imgui
from gui.debug_pane import debug_panel
from gui.pipeline import pipeline_panel
from gui.top_menu import top_menu_bar
from gui.video_timeline import video_panel

def gui():
    imgui.new_frame()
    debug_panel()
    top_menu_bar()
    video_panel()
    pipeline_panel()
    imgui.show_test_window()
