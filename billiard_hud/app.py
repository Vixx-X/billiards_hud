# -*- coding: utf-8 -*-

import cv2
import pyglet
from pyglet import gl

import imgui
from imgui.integrations.pyglet import create_renderer
from pygarrayimage.arrayimage import ArrayInterfaceImage

from gui import gui
from managers.debug import Debug
from managers.media import manager as Media
from pipeline import compile_pipeline, pipeline

WIDTH, HEIGHT = 1280, 720
image = None

def main():

    window = pyglet.window.Window(width=WIDTH, height=HEIGHT, resizable=True)
    gl.glClearColor(0, 0, 0, 1)
    imgui.create_context()
    impl = create_renderer(window)

    compile_pipeline()

    def update(dt):
        global image

        # Place ImGUI components
        gui()

        Debug.clear_times()

        if Media.ready():
            Debug.time("Reading")
            frame = Media.get_next_frame()
            Debug.time("Reading")

            if frame is not None:
                Debug.time("Processing")
                process_image = pipeline(frame)
                process_image = cv2.flip(process_image, 0) # OpenGL weird
                image = ArrayInterfaceImage(process_image)
                Debug.time("Processing")
                return

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
