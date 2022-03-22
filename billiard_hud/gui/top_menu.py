from managers.media import manager as Media
import imgui

def open_file():
    import tkinter as tk
    from tkinter import filedialog

    tk.Tk().withdraw() # we dont want full GUI

    filename = filedialog.askopenfilename(
        initialdir=".",
        title="Select the Billiard Game",
        filetypes=(
            ("video files", "*.mkv *.mp4"),
            ("all files", "*"),
        )
    )
    if filename:
        Media.open(filename)
        Media.play()

def save_file():
    import tkinter as tk
    from tkinter import filedialog

    tk.Tk().withdraw() # we dont want full GUI
    file = filedialog.asksaveasfile(
        initialfile = 'frame.jpg',
        defaultextension=".jpg",
        filetypes=(
            ("image files", "*.jpg *.png *.bmp"),
            ("all files", "*"),
        )
    )
    if file:
        Media.save(file.name)


def top_menu_bar():
    if imgui.begin_main_menu_bar():
        if imgui.begin_menu("File", True):

            clicked_open, selected_open = imgui.menu_item(
                "Open", 'Cmd+O', False, True
            )

            if clicked_open:
                open_file()

            if Media.ready() and Media.stopped:
                clicked_open, selected_open = imgui.menu_item(
                    "Save", 'Cmd+S', False, True
                )

                if clicked_open:
                    save_file()

            clicked_quit, selected_quit = imgui.menu_item(
                "Quit", 'Cmd+Q', False, True
            )

            if clicked_quit:
                exit(1)

            imgui.end_menu()
        imgui.end_main_menu_bar()
