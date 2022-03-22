from time import time


class DebugManager:
    logs = []
    texts = dict()
    timers = dict()
    ptime = None

    def clear_times(self):
        self.timers = dict()
    
    def clear_texts(self):
        self.texts = dict()

    def get_fps(self):
        timer = time()
        if self.ptime is None:
            self.ptime = timer
            return 0
        ret = 1/((timer - self.ptime))
        self.ptime = timer
        return ret

    def __call__(self, text):
        self.logs.append(text)

    def time(self, name):
        timer = time()
        start = self.timers.get(name)
        if not start:
            self.timers[name] = timer
        else:
            self.timers[name] = timer - start

    def text(self, name, text):
        self.texts[name] = text

    def get_times(self):
        return self.timers

    def get_texts(self):
        return self.texts

    def get_logs(self):
        return self.logs

Debug = DebugManager()
