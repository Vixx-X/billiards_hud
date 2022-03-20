import tkinter as tk
from tkinter import filedialog
from media_manager import manager

class VideoTimeLine(tk.Frame):
    video_state = 0

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        self.open_file_button = tk.Button(
            self,
            text="Open file",
            command=self.open_file_explorer,
        )
        self.play_stop_button = tk.Button(
            self,
            text="Play/Stop",
            command=self.toggle_video,
        )

        self.open_file_button.pack()
        self.play_stop_button.pack()

    def toggle_video(self):
        self.video_state = 1 - self.video_state
        if self.video_state:
            self.parent.play()
        else:
            self.parent.stop()

    def open_file_explorer(self):
        filename = filedialog.askopenfilename(
            initialdir=".",
            title="Select the Billiard Game",
            filetypes=(
                ("mkv files", "*.mkv"),
                ("mp4 files", "*.mp4"),
                ("all files", "*"),
            )
        )
        if filename:
            manager.open(filename)
