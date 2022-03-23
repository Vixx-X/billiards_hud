import cv2
import numpy as np
from managers.balls import manager as BallManager
from managers.debug import Debug
from managers.table import manager as TableManager


class Stage:
    id = ""

    def __init__(self, name):
        self.id = name

    def run(self, img, draw=False):
        return img

    def filter_ui(self):
        pass


class PipelineManager:
    show_detections = True
    selected_stage = None
    stages_output = {}
    stages = {}
    stages_id = []

    _iter = None

    def __iter__(self):
        self._iter = self.stages_id.__iter__()
        return self

    def __next__(self):
        name = self._iter.__next__()
        return self.stages[name]

    def __call__(self, name, stage=Stage):
        if name in self.stages:
            raise Exception(f"There is already a {name}")

        self.stages_id.append(name)
        self.stages[name] = stage(name)
        if not self.selected_stage:
            self.selected_stage = name

    def clear(self):
        self.stages_output = {}

    def select_stage(self, stage):
        self.selected_stage = stage

    def get_image(self):
        if self.selected_stage not in self.stages_output:
            raise Exception(f"Stage: ({self.selected_stage}) does not exists")

        out = self.stages_output[self.selected_stage]

        if len(out.shape) == 2:
            out = cv2.cvtColor(out, cv2.COLOR_GRAY2RGB)

        if not self.show_detections:
            return out

        out = draw_detections(out)

        if TableManager.fake_perspective:
            new_p =[
                    [0, 0],
                    [out.shape[1], 0],
                    [0, out.shape[0]],
                    [out.shape[1], out.shape[0]],
                ]

            old_p = [ x[0] for x in TableManager.get_points() ]

            mnnew_p = sorted(new_p, key=lambda k: (k[1] + k[0]))
            mnold_p = sorted(old_p, key=lambda k: (k[1] + k[0]))

            snew_p = [mnnew_p[0]] + sorted([i for i in new_p if i not in [mnnew_p[0], mnnew_p[3]] ], key=lambda k: (k[1], k[0])) + [mnnew_p[3]]
            sold_p = [mnold_p[0]] + sorted([i for i in old_p if i not in [mnold_p[0], mnold_p[3]] ], key=lambda k: (k[1], k[0])) + [mnold_p[3]]

            nsnew_p = np.float32(snew_p)
            nsold_p = np.float32(sold_p)

            # col = [
            #     (13, 128, 79),
            #     (13, 128, 255),
            #     (323, 128, 255),
            #     (13, 232, 23),
            # ]
            # for idx, point in enumerate(nsnew_p):
            #     cv2.circle(
            #         out,
            #         (int(point[0]), int(point[1])),
            #         30,
            #         col[idx],
            #         -1,
            #     )

            # for idx, point in enumerate(nsold_p):
            #     cv2.circle(
            #         out,
            #         (int(point[0]), int(point[1])),
            #         30,
            #         col[idx],
            #         -1,
            #     )

            M = cv2.getPerspectiveTransform(nsold_p, nsnew_p)
            out = cv2.warpPerspective(out, M, (out.shape[1], out.shape[0]))
        return out

    def run(self, name, img):
        out = self.stages[name].run(img, self.selected_stage == name)
        self.stages_output[name] = out
        return out


def draw_detections(img):
    BallManager.draw(img)
    TableManager.draw(img)
    return img


manager = PipelineManager()
