# -*- coding: utf-8 -*-

import pyglet
from pyglet import gl

import imgui
from imgui.integrations.pyglet import create_renderer
from pygarrayimage.arrayimage import ArrayInterfaceImage

from gui import gui
from managers.media import manager as Media

WIDTH, HEIGHT = 1280, 720
image = None

def main():

    window = pyglet.window.Window(width=WIDTH, height=HEIGHT, resizable=True)
    gl.glClearColor(1, 1, 1, 1)
    imgui.create_context()
    impl = create_renderer(window)

    def update(dt):
        global image

        # Place ImGUI components
        gui()

        if Media.ready():
            frame = Media.get_next_frame()
            image = ArrayInterfaceImage(frame)
        else:
            image = None


    def draw(dt):
        global image

        update(dt)
        window.clear()
        if image is not None:
            image.blit(0, 0, 0)
        imgui.render()
        impl.render(imgui.get_draw_data())

    pyglet.clock.schedule_interval(draw, 1/120.)
    pyglet.app.run()
    impl.shutdown()

if __name__=="__main__":
    main()
