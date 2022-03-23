from filters import (
    BlurStage,
    CloseStage,
    MaskStage,
    RedBallDetectorStage,
    RedBallMaskStage,
    ContourStage,
    WhiteBallDetectorStage,
    WhiteBallMaskStage,
    YellowBallDetectorStage,
    YellowBallMaskStage,
    CannyStage,
    HoughLinesStage,
    PaloMaskStage,
)
from managers.pipeline import manager as Pipeline
from managers.collision import manager as Collision


def compile_pipeline():
    Pipeline("Original")
    Pipeline("Blur", BlurStage)
    Pipeline("Mask", MaskStage)
    Pipeline("Closing", CloseStage)

    Pipeline("Table Detector", ContourStage)

    Pipeline("Red Ball Mask", RedBallMaskStage)
    Pipeline("Red Ball Detector", RedBallDetectorStage)

    Pipeline("White Ball Mask", WhiteBallMaskStage)
    Pipeline("White Ball Detector", WhiteBallDetectorStage)

    Pipeline("Yellow Ball Mask", YellowBallMaskStage)
    Pipeline("Yellow Ball Detector", YellowBallDetectorStage)

    Pipeline("Canny", CannyStage)
    Pipeline("Palo Mask", PaloMaskStage)
    Pipeline("Hough Lines", HoughLinesStage)

    Pipeline("Stick Detector")


def pipeline(img):
    original = Pipeline.run("Original", img)

    # preprocesing
    blur_img = Pipeline.run("Blur", original)
    mask_img = Pipeline.run("Mask", blur_img)
    closing_image = Pipeline.run("Closing", mask_img)

    # masked_img = Pipeline.run("Masking", (original, closing_image))

    # detectors stages

    # table
    Pipeline.run("Table Detector", (original, closing_image))

    # palo
    palo_mask = Pipeline.run("Palo Mask", blur_img)
    canny_image = Pipeline.run("Canny", palo_mask)
    Pipeline.run("Hough Lines", (original, palo_mask))

    # balls
    red_ball_mask = Pipeline.run("Red Ball Mask", blur_img)
    Pipeline.run("Red Ball Detector", (original, red_ball_mask))

    white_ball_mask = Pipeline.run("White Ball Mask", blur_img)
    Pipeline.run("White Ball Detector", (original, white_ball_mask))

    yellow_ball_mask = Pipeline.run("Yellow Ball Mask", blur_img)
    Pipeline.run("Yellow Ball Detector", (original, yellow_ball_mask))

    # stick
    Pipeline.run("Stick Detector", closing_image)


def get_result():
    Collision.run()
    return Pipeline.get_image()
