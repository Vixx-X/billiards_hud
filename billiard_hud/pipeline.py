from filters import BlurStage, CloseStage, MaskStage, HoughCirclesStage, MaskingStage
from managers.pipeline import manager as Pipeline


def compile_pipeline():
    Pipeline("Original")

    Pipeline("Blur", BlurStage)
    Pipeline("Mask", MaskStage)
    Pipeline("Closing", CloseStage)
    # Pipeline("Masking", MaskingStage)

    Pipeline("HoughCircles", HoughCirclesStage)
    Pipeline("Contour")
    Pipeline("HoughLines")


def pipeline(img):
    original = Pipeline.run("Original", img)

    # preprocesing
    blur_img = Pipeline.run("Blur", original)
    mask_img = Pipeline.run("Mask", blur_img)
    closing_image = Pipeline.run("Closing", mask_img)
    # masked_img = Pipeline.run("Masking", (original, closing_image))

    # detectors stages
    Pipeline.run("HoughCircles", closing_image)
    Pipeline.run("Contour", closing_image)
    Pipeline.run("HoughLines", closing_image)

    return Pipeline.get_image()



