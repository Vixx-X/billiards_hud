# -*- coding: utf-8 -*-

import pyglet
from pyglet import gl

import imgui
from imgui.integrations.pyglet import create_renderer
from pyglet.gl.gl import GLubyte

from gui import gui
from managers.media import manager as Media

WIDTH, HEIGHT = 1280, 720

def main():

    window = pyglet.window.Window(width=WIDTH, height=HEIGHT, resizable=True)
    gl.glClearColor(1, 1, 1, 1)
    imgui.create_context()
    impl = create_renderer(window)

    def update(dt):
        # Place ImGUI components
        gui()

        if Media.ready():
            frame = Media.get_next_processed_frame()
            w, h, c = frame.shape
            rawData = (GLubyte * w*h*c)(*frame.flatten())
            image_data = pyglet.image.ImageData(frame, w, h, 'BGR', rawData)
            image_data.blit(0,0)


    def draw(dt):
        update(dt)
        window.clear()
        imgui.render()
        impl.render(imgui.get_draw_data())

    pyglet.clock.schedule_interval(draw, 1/60.)
    pyglet.app.run()
    impl.shutdown()

if __name__=="__main__":
    main()
