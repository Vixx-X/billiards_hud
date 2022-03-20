# -*- coding: utf-8 -*-
import cv2
import glfw
import OpenGL.GL as gl

import imgui
from imgui.integrations.glfw import GlfwRenderer

from gui import gui

from managers.media import manager as Media

WIDTH, HEIGHT = 1280, 720

def convertMat2Tex(mat):
    # convert to RGB
    # mat = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)
    # flip for GL
    # mat = cv2.flip(mat, -1)
    # return data
    return mat

bitmap_tex = None
def blit_image(x,y,img,r,g,b):
    global bitmap_tex

    # get texture data
    w,h,_ = img.shape
    data = img

    # create texture object
    if bitmap_tex == None:
        bitmap_tex = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, bitmap_tex)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
    gl.glTexImage2D(gl.GL_TEXTURE_2D,0,gl.GL_RGB,w,h,0,gl.GL_BGR,gl.GL_UNSIGNED_BYTE,data)

    # save and set model view and projection matrix
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glPushMatrix()
    gl.glLoadIdentity()
    gl.glOrtho(0, w, 0, h, -1, 1)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glPushMatrix()
    gl.glLoadIdentity()

    # enable blending
    # gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    # gl.glEnable(gl.GL_BLEND)

    # draw textured quad
    gl.glColor3f(r,g,b)

    gl.glEnable(gl.GL_TEXTURE_2D)
    gl.glBegin(gl.GL_QUADS)
    gl.glTexCoord2f(0, 1)
    gl.glVertex2f(x, y)
    gl.glTexCoord2f(1, 1)
    gl.glVertex2f(x+w, y)
    gl.glTexCoord2f(1, 0)
    gl.glVertex2f(x+w, y+h)
    gl.glTexCoord2f(0, 0)
    gl.glVertex2f(x, y+h)
    gl.glEnd()
    gl.glDisable(gl.GL_TEXTURE_2D)

    # restore matrices
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glPopMatrix()
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glPopMatrix()

    # disable blending
    # gl.glDisable(gl.GL_BLEND)

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

        # Get texture from video frame
        if Media.ready():
            frame = Media.get_next_processed_frame()
            texture = convertMat2Tex(frame)
            blit_image(0, 0, texture, 1., 1., 1.)
        else:
            gl.glClearColor(1., 1., 1., 1)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        # Place ImGUI components
        gui()

        # Render gui and video
        imgui.render()
        impl.render(imgui.get_draw_data())

        # Swap front and back buffers
        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()


def impl_glfw_init():
    width, height = WIDTH, HEIGHT
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
