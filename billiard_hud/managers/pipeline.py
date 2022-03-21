
class Stage:
    id = ""

    def __init__(self, name):
        self.id = name

    def run(self, img):
        return img

    def filter_ui(self):
        pass


class PipelineManager:
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

    def clear(self):
        self.stages_output = {}

    def select_stage(self, stage):
        self.selected_stage = stage

    def get_image(self):
        if self.selected_stage not in self.stages_output:
            raise Exception(f"Stage: ({self.selected_stage}) does not exists")
        return self.stages_output[self.selected_stage]

    def run(self, name, img):
        out = self.stages[name].run(img)
        self.stages_output[name] = out
        return out


manager = PipelineManager()
