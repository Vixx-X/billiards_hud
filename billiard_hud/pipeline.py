from filters import BlurStage, CloseStage, MaskStage
from managers.pipeline import manager as Pipeline


def compile_pipeline():
    Pipeline("Original")

    Pipeline("Blur", BlurStage)
    Pipeline("Mask", MaskStage)
    Pipeline("Opening", CloseStage)

    Pipeline("HoughCircles")
    Pipeline("Contour")
    Pipeline("HoughLines")

    Pipeline("Output")


def pipeline(img):
    original = Pipeline.run("Original", img)

    # preprocesing
    blur_img = Pipeline.run("Blur", original)
    mask_img = Pipeline.run("Mask", blur_img)
    opening_image = Pipeline.run("Opening", mask_img)

    # detectors stages
    Pipeline.run("HoughCircles", opening_image)
    Pipeline.run("Contour", opening_image)
    Pipeline.run("HoughLines", opening_image)

    last_image = Pipeline.get_image()
    return Pipeline.run("Output", original if last_image is None else last_image)



