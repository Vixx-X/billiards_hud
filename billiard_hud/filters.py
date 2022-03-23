import cv2
import imgui
from managers.pipeline import Stage
from managers.debug import Debug
import numpy as np
import colorsys


class BlurStage(Stage):

    iterations = 3
    kernel_shape = (3, 3)

    def run(self, img, draw):
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

    def run(self, img, draw):
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

    def run(self, img, draw):
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


# class CannyStage(Stage):
#     thresh = 30

#     def run(self, img, draw):
#         return cv2.Canny(img, self.thresh / 2, self.thresh)

#     def filter_ui(self):
#         changed, value = imgui.slider_float(
#             "thresh",
#             value=self.thresh,
#             min_value=1.0,
#             max_value=100.0,
#             format="%f",
#         )

#         if changed:
#             self.thresh = value


class RedBallStage(MaskStage):
    lower = np.array([147.0, 175.0, 35.0])
    upper = np.array([207.0, 255.0, 255.0])


class YellowBallStage(MaskStage):
    # lower = np.array([0.0, 130.0, 140.0])
    lower = np.array([0.0, 130.0, 100.0])
    upper = np.array([30.0, 255.0, 255.0])


class WhiteBallStage(MaskStage):
    lower = np.array([0.0, 0.0, 160.0])
    upper = np.array([30.0, 115.0, 255.0])


class ContourStage(Stage):
    counter_stage = None
    eps = 0.1

    def run(self, images, draw):
        (original, img) = images
        # if self.counter_stage is None:
        #     self.counter_stage = img

        # avg = cv2.add(self.counter_stage, img) / 2

        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, 2)
        max_contour = 0

        for idx, contour in enumerate(contours):
            M = cv2.moments(contour)
            if M["m00"] > max_contour:
                max_contour = idx

        if draw:
            cnt = contours[max_contour]
            epsilon = self.eps * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            cv2.drawContours(original, contours, -1, (255, 0, 0), 3)
            cv2.drawContours(original, [approx], -1, (125, 125, 0), 3)
        return original

    def filter_ui(self):
        changed, value = imgui.slider_float(
            "EPS",
            value=self.eps,
            min_value=0,
            max_value=1,
            format="%f",
        )
        if changed:
            self.eps = value
