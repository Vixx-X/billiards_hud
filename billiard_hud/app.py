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
from pipeline import compile_pipeline, pipeline, get_result

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

                down = 1/Debug.scale_factor
                half_frame = cv2.resize(frame, None, fx=down, fy=down)

                pipeline(half_frame)

                process_image = get_result()
                half_out = cv2.flip(process_image, 0) # OpenGL weird

                up = Debug.scale_factor
                out = cv2.resize(half_out, None, fx=up, fy=up)
                Debug.time("Processing")

                Debug.time("Bliting to Tex")
                image = ArrayInterfaceImage(out)
                Debug.time("Bliting to Tex")
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

    pyglet.clock.schedule_interval(draw, 1/60.)
    pyglet.app.run()
    impl.shutdown()

if __name__=="__main__":
    main()
