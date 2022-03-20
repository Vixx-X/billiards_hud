# -*- coding: utf-8 -*-
import glfw
import OpenGL.GL as gl

import imgui
from imgui.integrations.glfw import GlfwRenderer

def open_file():
    import tkinter as tk
    from tkinter import filedialog

    tk.Tk().withdraw() # we dont want full GUI

    filename = filedialog.askopenfilename(
        initialdir=".",
        title="Select the Billiard Game",
        filetypes=(
            ("mkv files", "*.mkv"),
            ("mp4 files", "*.mp4"),
            ("all files", "*"),
        )
    )
    if filename:
        manager.open(filename)

def debug_panel():
    imgui.begin("Debug Metric")
    imgui.text("Bar")
    imgui.text_ansi("B\033[31marA\033[mnsi ")
    imgui.text_ansi_colored("Eg\033[31mgAn\033[msi ", 0.2, 1., 0.)
    imgui.extra.text_ansi_colored("Eggs", 0.2, 1., 0.)
    imgui.end()

def menu_bar():
    if imgui.begin_main_menu_bar():
        if imgui.begin_menu("File", True):

            clicked_open, selected_open = imgui.menu_item(
                "Open", 'Cmd+O', False, True
            )

            if clicked_open:
                open_file()

            clicked_quit, selected_quit = imgui.menu_item(
                "Quit", 'Cmd+Q', False, True
            )

            if clicked_quit:
                exit(1)

            imgui.end_menu()
        imgui.end_main_menu_bar()

def gui():
    imgui.new_frame()
    menu_bar()
    debug_panel()
    imgui.show_test_window()

def main():
    # Create a windowed mode window and its OpenGL context
    imgui.create_context()
    window = impl_glfw_init()
    impl = GlfwRenderer(window)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll for and process events
        glfw.poll_events()
        impl.process_inputs()

        # Place ImGUI
        gui()

        # Get texture from video frame
        gl.glClearColor(1., 1., 1., 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        # Render gui and video
        imgui.render()
        impl.render(imgui.get_draw_data())

        # Swap front and back buffers
        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()


def impl_glfw_init():
    width, height = 1280, 720
    window_name = "Project #3 - Billiard HUD"

    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(
        int(width), int(height), window_name, None, None
    )
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        exit(1)

    return window
