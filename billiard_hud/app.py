# -*- coding: utf-8 -*-
import cv2
import glfw
import OpenGL.GL as gl

import imgui
from imgui.integrations.glfw import GlfwRenderer

from gui import gui

from managers.media import manager as Media


def convertMat2Tex(mat):
    # convert to RGB
    mat = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)
    # flip for GL
    mat = cv2.flip(mat, -1)
    # return data
    return mat

def refresh2d(width, height):
    gl.glViewport(0, 0, width, height)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    gl.glMatrixMode (gl.GL_MODELVIEW)
    gl.glLoadIdentity()

def draw_rect(x, y, width, height):
    gl.glBegin(gl.GL_QUADS)                 # start drawing a rectangle
    gl.glVertex2f(x, y)                     # bottom left point
    gl.glVertex2f(x + width, y)             # bottom right point
    gl.glVertex2f(x + width, y + height)    # top right point
    gl.glVertex2f(x, y + height)            # top left point
    gl.glEnd()

def main():
    # Create a windowed mode window and its OpenGL context
    imgui.create_context()
    window = impl_glfw_init()
    impl = GlfwRenderer(window)


    # texID = gl.glGenTextures(1)
    # gl.glBindTexture(gl.GL_TEXTURE_2D, texID)
    # gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
    # gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
    # gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP)
    # gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll for and process events
        glfw.poll_events()
        impl.process_inputs()

        # Place ImGUI
        gui()

        # clear the screen
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        # refresh2d(1000, 1000)                    # set mode to 2d
        gl.glColor3f(0.0, 0.0, 1.0)              # set color to blue
        draw_rect(10, 10, 200, 100)              # rect at (10, 10) with width 200, height 100


        # Get texture from video frame
        # if Media.ready():
        #     frame = Media.get_next_processed_frame()
        #     texture = convertMat2Tex(frame)
        #     height, width, _ = texture.shape
        #     gl.glTexImage2D(
        #         gl.GL_TEXTURE_2D, 0, gl.GL_RGB, width, height,
        #         0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, texture
        #     );
        #     gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
        #     # gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        #     gl.glBindTexture(gl.GL_TEXTURE_2D, texID)
        #     gl.gl.glBegin(gl.GL_QUADS)
        #     gl.glTexCoord2f(0, 0); gl.glVertex2f(-1, -1)
        #     gl.glTexCoord2f(0, 1); gl.glVertex2f(-1, 1)
        #     gl.glTexCoord2f(1, 1); gl.glVertex2f(1, 1)
        #     gl.glTexCoord2f(1, 0); gl.glVertex2f(1, -1)
        #     gl.glEnd()

        # else:
        #     gl.glClearColor(1., 1., 1., 1)
        #     gl.glClear(gl.GL_COLOR_BUFFER_BIT)

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

if __name__=="__main__":
    main()
