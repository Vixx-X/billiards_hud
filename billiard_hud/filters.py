
import cv2
import imgui
from managers.pipeline import Stage
import numpy as np
import colorsys


class BlurStage(Stage):

    iterations = 3
    kernel_shape = (3, 3)

    def run(self, img):
        for _ in range(self.iterations):
            img = cv2.blur(img, self.kernel_shape)
        return img

    def filter_ui(self):
        changed, value = imgui.slider_int(
            "Iterations",
            value=self.iterations,
            min_value=0,
            max_value=10,
        )
        if changed:
            self.iterations = value

        changed, value = imgui.slider_int2(
            "Kernel shape",
            value0=self.kernel_shape[0],
            value1=self.kernel_shape[1],
            min_value=3,
            max_value=27,
            format="%d",
        )
        if changed:
            self.kernel_shape = value




class MaskStage(Stage):

    lower = np.array([110.,50.,40.])
    upper = np.array([130.,255.,255.])

    def run(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Here we are defining range of bluecolor in HSV
        # This creates a mask of blue coloured 
        # objects found in the frame.
        ret = cv2.inRange(hsv, self.lower, self.upper)
        return ret

    def filter_ui(self):
        changed, value = imgui.color_edit3(
            "Lower",
            *colorsys.hsv_to_rgb(*(self.lower/255.))
        )
        if changed:
            self.lower = np.clip(np.array(
                colorsys.rgb_to_hsv(*np.array(value))
            ) * 255, 0, 255)


        changed, value = imgui.color_edit3(
            "Upper",
            *colorsys.hsv_to_rgb(*(self.upper/255.))
        )
        if changed:
            self.upper = np.clip(np.array(
                colorsys.rgb_to_hsv(*np.array(value))
            ) * 255, 0, 255)



class CloseStage(Stage):

    kernel_shape = (9, 9)

    def run(self, img):
        return cv2.morphologyEx(
            img,
            cv2.MORPH_CLOSE,
            cv2.getStructuringElement(cv2.MORPH_CROSS, self.kernel_shape),
        )

    def filter_ui(self):
        changed, value = imgui.slider_int2(
            "Kernel shape",
            value0=self.kernel_shape[0],
            value1=self.kernel_shape[1],
            min_value=3,
            max_value=27,
            format="%d",
        )
        if changed:
            self.kernel_shape = value
