import cv2

class Stage:
    id = ""

    def __init__(self, name):
        self.id = name

    def run(self, img):
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
        self.selected_stage = name

    def clear(self):
        self.stages_output = {}

    def select_stage(self, stage):
        self.selected_stage = stage

    def get_image(self):
        if self.stages_id[-1] == self.selected_stage:
            # last image will call this as its input
            return None

        if self.selected_stage not in self.stages_output:
            raise Exception(f"Stage: ({self.selected_stage}) does not exists")
        return self.stages_output[self.selected_stage]

    def run(self, name, img):
        out = self.stages[name].run(img)
        aux = out
        if len(out.shape) == 2:
            aux = cv2.cvtColor(out, cv2.COLOR_GRAY2RGB)
        self.stages_output[name] = aux
        return out


manager = PipelineManager()
