import enum
import cv2
import time
import numpy as np
import math

all_images = tuple()

def clean_draw():
    global all_images
    all_images = tuple()

def draw(img, text=None):
    global all_images
    if text:
        img = img.copy()
        cv2.putText(img, text, (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (175, 0, 200), 3)

    all_images += (img,)

def draw_all():
    global all_images
    show_images(all_images)

def get_centroid(contour):
    M = cv2.moments(contour)
    if M['m00'] == 0:
        return (None, None)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    return (cx, cy)

def angle_diff(angle1, angle2):
    rest = abs(angle2 - angle1)
    return min(rest, 255 - rest)

def is_red(hsv_color):
    return hsv_color[0] > 160
    # return angle_diff(hsv_color[0], 255) <= 20

def is_yellow(hsv_color):
    return 30 > hsv_color[0] > 5
    # return angle_diff(hsv_color[0], 55) <= 13

def is_white(hsv_color):
    return hsv_color[1] < 100
    # return hsv_color[0] < 20 and hsv_color[1] < 20 and hsv_color[2] > 240

RADIUS = 5
class BallColor(enum.Enum):
    ERROR = 0
    RED = 1
    YELLOW = 2
    WHITE = 3

    def get_BGR(self):
        if self == self.RED:
            return (0, 0, 255)
        if self == self.YELLOW:
            return (0, 255, 255)
        if self == self.WHITE:
            return (255, 255, 255)
        return (0, 0, 0)

class Ball:
    x = 0
    y = 0
    r = RADIUS
    color = BallColor.ERROR

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def is_intercepting(self, ball):
        (x1, y1), (x2, y2) = (self.x, self.y), (ball.x, ball.y)
        return (x2 - x1)**2 + (y2 - y1)**2 <= (2*RADIUS)**2

    def is_overlapping(self, ball):
        (x1, y1), (x2, y2) = (self.x, self.y), (ball.x, ball.y)
        return (x2 - x1)**2 + (y2 - y1)**2 <= (RADIUS/2)**2


def findBall(original_image, outer_canny):
    contours, _ = cv2.findContours(outer_canny, 1, 2)
    cont_img = original_image.copy()
    cv2.drawContours(cont_img, contours, -1, (0, 255, 0), 3)
    draw(cont_img, f"out-cont ({len(contours)})")

    def is_ball(cnt):
        (x, y) = get_centroid(cnt)
        length = cv2.arcLength(cnt, True)
        return not(x is None or y is None or length > 40 or length < 30)

    # filter (close contour, not all collinear)
    ball_centroids = [get_centroid(cnt) for cnt in contours if is_ball(cnt)]

    # filter overlapping balls
    balls = []
    for possible_ball in ball_centroids:
        p_ball = Ball(possible_ball[0], possible_ball[1])
        for ball in balls:
            if ball.is_overlapping(p_ball):
                break
        else:
            balls.append(p_ball)

    # classify by color
    K = 2
    ball_img = original_image.copy()
    for ball in balls:
        x, y = ball.x, ball.y
        neigh = original_image[y-K: y+K+1, x-K: x+K+1]
        avg_color = np.average(np.average(neigh, axis=0), axis=0)

        uni_mat = np.uint8([[[avg_color[0], avg_color[1], avg_color[2]]]])
        color = cv2.cvtColor(uni_mat, cv2.COLOR_BGR2HSV)[0][0]

        if is_white(color):
            ball.color = BallColor.WHITE
        elif is_red(color):
            ball.color = BallColor.RED
        elif is_yellow(color):
            ball.color = BallColor.YELLOW

    # filter unclassified balls
    balls = [ball for ball in balls if ball.color != BallColor.ERROR]

    # drawing balls
    ball_img = original_image.copy()
    for ball in balls:
        ball_img = cv2.circle(
            ball_img,
            (ball.x, ball.y),
            RADIUS, ball.color.get_BGR(),
            -1
        )

    draw(ball_img, f"balls {len(balls)}")


    cnt = contours[-1]
    epsilon = 0.05*cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    p_cont_img = img.copy()
    cv2.drawContours(p_cont_img, [approx], -1, (125, 125, 0), 3)
    draw(p_cont_img, f"outer contour")


def pipeline(img):
    clean_draw()
    draw(img, "original")

    blur = cv2.blur(img, (3, 3))
    blur = cv2.blur(blur, (3, 3))
    blur = cv2.blur(blur, (3, 3))
    draw(blur, "blur")

    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([110,50,40])
    upper_blue = np.array([130,255,255])

    # Here we are defining range of bluecolor in HSV
    # This creates a mask of blue coloured 
    # objects found in the frame.
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    draw(mask, "mask")

    close_mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_CROSS,(9,9))
    )
    draw(close_mask, "close")

    outer_canny = cv2.Canny(mask, 10, 20)
    draw(outer_canny, "outer canny")

    findBall(img, outer_canny)
    findBall(img, close_mask)

    original_masked = cv2.bitwise_or(blur, blur, mask=close_mask)
    draw(original_masked, "original_masked")

    canny = cv2.Canny(original_masked, 10, 20)
    draw(canny, "canny")

    thicking_canny = cv2.dilate(
        canny,
        np.ones(shape=(3,3)),
    )
    draw(thicking_canny, "thic canny")

    contours, _ = cv2.findContours(thicking_canny, 1, 2)
    cont_img = img.copy()
    cv2.drawContours(cont_img, contours, -1, (0, 255, 0), 3)
    draw(cont_img, f"all contours ({len(contours)})")

    draw_all()
    return img

    cnt = contours[32]
    cont_img = img.copy()
    cv2.drawContours(cont_img, [cnt], -1, (0, 255, 0), 3)
    draw(cont_img, f"choosen countour")

    epsilon = 0.1*cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    p_cont_img = img.copy()
    cv2.drawContours(p_cont_img, [approx], -1, (0, 255, 255), 3)
    draw(p_cont_img, "new contour")

    draw_all()

    return img

    lines = cv2.HoughLines(img, 1, np.pi / 180, 150, None, 0, 0)

    if lines is not None:
        print(len(lines))
        for line in lines:
            rho = line[0][0]
            theta = line[0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv2.line(img, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)

    return img

def show_images(images):

    images = [cv2.cvtColor(img, cv2.COLOR_GRAY2BGR) if img.ndim == 2 else img for img in images]

    nCol = 4
    cnt = 0
    row_images = []
    row_image = []
    for img in images:
        if cnt == 4:
            cnt = 0
            row_images.append(row_image)
            row_image = []
        row_image.append(img)
        cnt += 1
    if len(row_image):
        shape = row_image[0].shape
        dtype = row_image[0].dtype
        for _ in range(len(row_image), nCol):
            row_image.append(np.zeros(shape, dtype))
        row_images.append(row_image)

    rows = [np.concatenate(row, axis=1) for row in row_images]
    img = np.concatenate(rows)
    cv2.imshow('Frame', img)


if __name__ == "__main__":
    # Create a VideoCapture object and read from input file
    cap = cv2.VideoCapture('../../media/Three-Cushion Billiards Top View [F4SqfOvE21g].mkv')
    # cap = cv2.VideoCapture(0)
    pTime = time.time()

    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error opening video file")

    # Read until video is completed
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, img = cap.read()
        if ret == True:

            img = cv2.resize(img, (0, 0), None, 0.25, 0.25)

            frame = pipeline(img)

            # cTime = time.time()
            # fps = 1 / (cTime - pTime)
            # pTime = cTime
            # cv2.putText(frame, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

            # Display the resulting frame
            # cv2.imshow('Frame', frame)

            # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break

    # When everything done, release
    # the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()

