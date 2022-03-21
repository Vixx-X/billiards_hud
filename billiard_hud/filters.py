
import cv2
import imgui
from managers.pipeline import Stage
import numpy as np


class BlurStage(Stage):

    iterations = 3
    kernel_shape = (3, 3)

    def run(self, img):
        for _ in range(self.iterations):
            img = cv2.blur(img, self.kernel_shape)
        return img

    def filter_ui(self):
        pass



class MaskStage(Stage):

    lower = np.array([110.,50.,40.])
    upper = np.array([130.,255.,255.])

    def run(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Here we are defining range of bluecolor in HSV
        # This creates a mask of blue coloured 
        # objects found in the frame.
        return cv2.inRange(hsv, self.lower, self.upper)

    def filter_ui(self):
        changed, value = imgui.color_edit3(
            "Lower",
            *(self.lower/255.),
            imgui.COLOR_EDIT_HSV
        )
        if changed:
            breakpoint()
            self.lower = np.array(value)

        color = [
            float(0.),
            float(0.),
            float(0.),
        ]

        changed, value = imgui.color_edit3(
            "Upper",
            # *(self.upper/255.),
            # *(
            #     float(self.upper[0])/255,
            #     float(self.upper[1])/255,
            #     float(self.upper[2])/255,
            # ),
            *color,
            imgui.COLOR_EDIT_HSV
        )
        if changed:
            self.upper = np.array(value)



class CloseStage(Stage):

    kernel_shape = (9, 9)

    def run(self, img):
        return cv2.morphologyEx(
            img,
            cv2.MORPH_CLOSE,
            cv2.getStructuringElement(cv2.MORPH_CROSS, self.kernel_shape),
        )

    def filter_ui(self):
        pass
