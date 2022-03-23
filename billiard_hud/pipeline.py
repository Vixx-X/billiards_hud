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
    NegativeStage,
    AndStage,
    StickMaskStage,
    OpenStage,
    ErosionStage,
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

    # Pipeline("Canny", CannyStage)
    # Pipeline("Negative Mask", NegativeStage)
    Pipeline("Open Mask", OpenStage)
    # Pipeline("Erosion Mask", ErosionStage)
    # Pipeline("And Mask", AndStage)
    Pipeline("Stick Mask", StickMaskStage)
    Pipeline("Stick Detector", HoughLinesStage)


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

    # balls
    red_ball_mask = Pipeline.run("Red Ball Mask", blur_img)
    Pipeline.run("Red Ball Detector", (original, red_ball_mask))

    white_ball_mask = Pipeline.run("White Ball Mask", blur_img)
    Pipeline.run("White Ball Detector", (original, white_ball_mask))

    yellow_ball_mask = Pipeline.run("Yellow Ball Mask", blur_img)
    Pipeline.run("Yellow Ball Detector", (original, yellow_ball_mask))

    # stick
    stick_mask = Pipeline.run("Stick Mask", original)
    # negative_mask = Pipeline.run("Negative Mask", white_ball_mask)
    close_mask = Pipeline.run("Closing", stick_mask)
    # erosion_mask = Pipeline.run("Erosion Mask", open_mask)
    # and_mask = Pipeline.run("And Mask", (erosion_mask, stick_mask))
    Pipeline.run("Stick Detector", (original, close_mask))


def get_result():
    Collision.run()
    return Pipeline.get_image()
