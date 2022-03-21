import cv2

class MediaManager:
    video_filename = None
    cap = None
    start = 0
    end = 0
    frame = None
    frame_id = start
    stopped = True

    def is_cam(self):
        return isinstance(self.video_filename, int)

    def ready(self):
        return self.cap and self.cap.isOpened()

    def read_stopped_frame(self):
        frame_id = self.frame_id

        ok, frame = self.cap.read()
        if not ok:
            self.frame = None
            return

        self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.set_frame(frame_id, 1)


    def open(self, filename):
        # filename = 0
        self.video_filename = filename
        self.cap = cv2.VideoCapture(self.video_filename)
        self.frame_size = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.end = self.frame_size - 1
        self.start = 0
        self.frame_id = 0


    def set_frame(self, frame_id, detph=0):
        self.frame_id = min(self.end, max(self.start, frame_id))
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.frame_id)

        if self.stopped and not detph:
            self.read_stopped_frame()

    def set_start(self, start):
        # validate inside video_filename timeline and before end
        self.start = min(max(start, 0), self.end)
        if start > self.frame_id:
            self.set_frame(start)

    def set_end(self, end):
        # validate inside video_filename timeline and after start
        self.end = max(min(self.frame_size - 1, end), self.start)
        if end > self.frame_id:
            self.set_frame(end)

    def close(self):
        if self.cap:
            self.cap.release()

    def play(self):
        self.stopped = False

    def stop(self):
        self.stopped = True

    def toggle(self):
        self.stopped = not self.stopped

    def read(self):
        if self.stopped:
            return

        if self.frame_id >= self.end and not self.is_cam():
            return

        ok, frame = self.cap.read()

        if not ok:
            self.frame = None
            return

        self.frame_id += 1

        if self.frame_id == self.end:
            self.close()

        self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def get_frame(self):
        return self.frame

    def get_next_frame(self):
        self.read()
        return self.get_frame()



manager = MediaManager()
