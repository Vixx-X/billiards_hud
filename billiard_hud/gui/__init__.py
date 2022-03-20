import imgui
from gui.debug_pane import debug_panel
from gui.top_menu import top_menu_bar

def gui():
    imgui.new_frame()
    top_menu_bar()
    debug_panel()
    imgui.show_test_window()
