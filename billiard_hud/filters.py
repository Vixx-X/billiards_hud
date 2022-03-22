import cv2
import imgui
from managers.pipeline import Stage
from managers.debug import Debug
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

    lower = np.array([110.0, 0.0, 0.0])
    upper = np.array([130.0, 255.0, 255.0])

    def run(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

        # Here we are defining range of bluecolor in HSV
        # This creates a mask of blue coloured
        # objects found in the frame.
        ret = cv2.inRange(hsv, self.lower, self.upper)
        return ret

    def filter_ui(self):
        changed, value = imgui.color_edit3(
            "Lower", *colorsys.hsv_to_rgb(*(self.lower / 255.0))
        )
        if changed:
            self.lower = np.clip(
                np.array(colorsys.rgb_to_hsv(*np.array(value))) * 255, 0, 255
            )

        changed, value = imgui.color_edit3(
            "Upper", *colorsys.hsv_to_rgb(*(self.upper / 255.0))
        )
        if changed:
            self.upper = np.clip(
                np.array(colorsys.rgb_to_hsv(*np.array(value))) * 255, 0, 255
            )


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


class MaskingStage(Stage):
    def run(self, images):
        img, mask = images
        return cv2.bitwise_or(img, img, mask=mask)

class HoughCirclesStage(Stage):
    method = cv2.HOUGH_GRADIENT
    dp = 1
    minDist = 20
    param1 = 50
    param2 = 40
    minRadius = 4
    maxRadius = 0

    def run(self, img):

        circles = cv2.HoughCircles(
            img,
            self.method,
            self.dp,
            self.minDist,
            param1=self.param1,
            param2=self.param2,
            minRadius=self.minRadius,
            maxRadius=self.maxRadius,
        )
        out = 0 if circles is None else len(circles)
        Debug.text("Circles", f"{out}")
        Debug.text(
            "Circles mindist",
            f"minDist: {self.minDist}, r1: {self.minRadius}, r2: {self.maxRadius} ",
        )
        # img = cv2.cvtColor(img, cv2.GRAY2RGB)
        if circles is not None:
            for i in circles:
                # draw the outer circle
                cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # draw the center of the circle
                cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)

        return img

    def filter_ui(self):
        changed, value = imgui.slider_float(
            "Min distance",
            value=self.minDist,
            min_value=1.,
            max_value=100.,
            format="%f",
        )

        if changed:
            self.minDist = value

#         changed, value = imgui.slider_int(
#             "DP",
#             value=self.dp,
#             min_value=1,
#             max_value=10,
#         )

#         if changed:
#             self.dp = value

        # changed, value = imgui.slider_int(
        #     "PARAM 1",
        #     value=self.param1,
        #     min_value=0,
        #     max_value=100,
        # )

        # if changed:
        #     self.param1 = value

        # changed, value = imgui.slider_int(
        #     "PARAM 2",
        #     value=self.param2,
        #     min_value=0,
        #     max_value=100,
        # )

        # if changed:
        #     self.param2 = value

        changed, (start, end) = imgui.drag_int2(
            label="Radius Range",
            value0=self.minRadius,
            value1=self.maxRadius,
            change_speed=1,
            min_value=0,
            max_value=50,
            format="%d",
        )

        if changed:
            self.minRadius = start
            self.maxRadius = end
