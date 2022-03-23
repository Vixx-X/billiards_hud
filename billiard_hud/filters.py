from cmath import inf
import math
import cv2
import imgui
from managers.pipeline import Stage
from managers.debug import Debug
import numpy as np
import colorsys

from managers.balls import manager as BallManager

from objects.balls import Ball, BallColor


class BlurStage(Stage):

    iterations = 3
    kernel_shape = (3, 3)

    def run(self, img, draw):
        for _ in range(self.iterations):
            img = cv2.GaussianBlur(img, self.kernel_shape, 0)
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


class CannyStage(Stage):
    thresh = 30

    def run(self, img, draw):
        return cv2.Canny(img, self.thresh / 2, self.thresh)

    def filter_ui(self):
        changed, value = imgui.slider_float(
            "thresh",
            value=self.thresh,
            min_value=1.0,
            max_value=100.0,
            format="%f",
        )

        if changed:
            self.thresh = value


class HoughLinesStage(Stage):

    rho = 1.48
    theta = np.pi / 180
    threshold = 100
    minLineLength = 60
    maxLineGap = 5.17

    def run(self, images, draw):
        original, img = images
        lines = cv2.HoughLinesP(
            img,  # Input edge image
            self.rho,  # Distance resolution in pixels
            self.theta,  # Angle resolution in radians
            threshold=self.threshold,  # Min number of votes for valid line
            minLineLength=self.minLineLength,  # Min allowed length of line
            maxLineGap=self.maxLineGap,  # Max allowed gap between line for joining them
        )
        lines_list = []
        out = 0 if lines is None else len(lines)
        Debug.text("Num of lines", f"{out}")
        if lines is not None:
            Debug.text("Lines", f"{lines}")
            lines = np.uint16(np.around(lines))
            if draw:
                for points in lines:
                    # Extracted points nested in the list
                    x1, y1, x2, y2 = points[0]
                    # Draw the lines joing the points
                    # On the original image
                    cv2.line(original, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    # Maintain a simples lookup list for points
                    lines_list.append([(x1, y1), (x2, y2)])
                    # draw the outer circle

                    # draw the center of the circle
                    # cv2.circle(original, (i[0], i[1]), 2, (0, 0, 255), 3)

        return original

    def filter_ui(self):
        changed, value = imgui.slider_float(
            "Resolution in pixels",
            value=self.rho,
            min_value=0,
            max_value=10,
            format="%f",
        )
        if changed:
            self.rho = value

        changed, value = imgui.slider_float(
            "Min Line Length",
            value=self.minLineLength,
            min_value=0,
            max_value=100,
            format="%f",
        )
        if changed:
            self.minLineLength = value

        changed, value = imgui.slider_float(
            "Max Line gap",
            value=self.maxLineGap,
            min_value=0,
            max_value=100,
            format="%f",
        )
        if changed:
            self.maxLineGap = value

        changed, value = imgui.slider_int(
            "Umbral",
            value=self.threshold,
            min_value=0,
            max_value=1000,
        )
        if changed:
            self.threshold = value


class BallDetectorStage(Stage):
    ball_color = BallColor.ERROR

    def run(self, images, draw):
        original, img = images

        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, 2)

        min_contour_error = float("inf")
        ball = None

        for contour in contours:
            M = cv2.moments(contour)
            area = M["m00"]
            if area:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                p_ball = Ball(cx, cy, color=self.ball_color)
                contour_error = abs(area - p_ball.r**2 * np.pi)
                if contour_error < min_contour_error:
                    min_contour_error = contour_error
                    ball = p_ball
                # if M["m00"] > ball.r**2 * np.pi:
                #     continue

        if ball is not None:
            BallManager.push(ball)

            if draw:
                cv2.circle(
                    original,
                    (ball.x, ball.y),
                    ball.r,
                    ball.color.get_BGR()[::-1],
                    -1,
                )

        return original


class RedBallMaskStage(MaskStage):
    lower = np.array([147.0, 175.0, 35.0])
    upper = np.array([207.0, 255.0, 255.0])


class RedBallDetectorStage(BallDetectorStage):
    ball_color = BallColor.RED


class YellowBallMaskStage(MaskStage):
    lower = np.array([0.0, 140.0, 100.0])
    upper = np.array([30.0, 255.0, 255.0])


class YellowBallDetectorStage(BallDetectorStage):
    ball_color = BallColor.YELLOW


class WhiteBallMaskStage(MaskStage):
    lower = np.array([0.0, 0.0, 160.0])
    upper = np.array([30.0, 97.0, 255.0])


class PaloMaskStage(MaskStage):
    # lower = np.array([0.0, 5.0, 88.0])
    # lower = np.array([0.0, 0.0, 30.0])
    lower = np.array([5.0, 13.0, 90.0])
    # upper = np.array([193.0, 100.0, 198.0])
    # upper = np.array([109.0, 120.0, 195.0])
    upper = np.array([21.0, 106.0, 255.0])


class WhiteBallDetectorStage(BallDetectorStage):
    ball_color = BallColor.WHITE


# class HoughLinesStage(BallDetectorStage):
#     ball_color = BallColor.WHITE


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
