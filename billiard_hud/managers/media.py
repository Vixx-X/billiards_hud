from time import sleep
import cv2
from threading import Thread

class MediaManager:
    video_filename = None
    cap = None
    start = 0
    end = 0
    frame = None
    frame_id = start
    stopped = True


    def ready(self):
        return self.cap and self.cap.isOpened()

    def open(self, filename):
        self.video_filename = filename
        self.cap = cv2.VideoCapture(self.video_filename)
        self.frame_size = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.end = self.frame_size - 1
        self.start = 0
        self.frame_id = 0

        # Thread(target=self.read, args=()).start()

    def set_frame(self, frame_id):
        self.frame = min(self.end, max(self.start, frame_id))
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.frame_id)

    def set_start(self, start):
        # validate inside video_filename timeline and before end
        self.start = min(max(start, 0), self.end)
        self.frame = max(start, self.frame_id)

    def set_end(self, end):
        # validate inside video_filename timeline and after start
        self.end = max(min(self.frame_size - 1, end), self.start)
        self.frame = min(end, self.frame_id)

    def close(self):
        if self.cap:
            self.cap.release()

    def play(self):
        self.stopped = False

    def stop(self):
        self.stopped = True

    def read(self):
        if self.stopped:
            self.frame = None
            return

        if self.frame_id >= self.end:
            self.frame = None
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
