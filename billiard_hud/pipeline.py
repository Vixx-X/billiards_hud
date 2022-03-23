from filters import BlurStage, CloseStage, MaskStage, RedBallDetectorStage, RedBallMaskStage, ContourStage
from managers.pipeline import manager as Pipeline


def compile_pipeline():
    Pipeline("Original")

    Pipeline("Blur", BlurStage)
    Pipeline("Mask", MaskStage)
    Pipeline("Closing", CloseStage)

    Pipeline("Red Ball Mask", RedBallMaskStage)
    Pipeline("Red Ball Detector", RedBallDetectorStage)

    Pipeline("Contour", ContourStage)
    Pipeline("HoughLines")


def pipeline(img):
    original = Pipeline.run("Original", img)

    # preprocesing
    blur_img = Pipeline.run("Blur", original)
    mask_img = Pipeline.run("Mask", blur_img)
    closing_image = Pipeline.run("Closing", mask_img)
    # masked_img = Pipeline.run("Masking", (original, closing_image))

    # detectors stages

    # balls
    red_ball_mask = Pipeline.run("Red Ball Mask", blur_img)
    Pipeline.run("Red Ball Detector", (original, red_ball_mask))

    Pipeline.run("Contour", (original, closing_image))
    Pipeline.run("HoughLines", closing_image)


def get_result():
    return Pipeline.get_image()
