from os import path, environ
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, askdirectory
from PIL import Image, ImageTk
import utils
import Map
# fix_height, fix_width = 640, 960
import Recorder

title = "Operational Map Alpha 2.71828"

if __name__ == "__main__":
    root = tk.Tk()
    root.title(title)
    # root.geometry("1280x750")
    main_panel = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
    main_panel.pack(expand=True)

    left_part = tk.Canvas(main_panel, width=350)
    left_part.image = Image.open('./icons/annri.jpg')
    left_part.image = ImageTk.PhotoImage(left_part.image)
    left_part.create_image(0, 0, image=left_part.image, anchor="nw", tags='icon')
    main_panel.add(left_part)

    Notebook = ttk.Notebook(root)
    Notebook.pack(expand=True)

    recorder_widget = Recorder.RecorderFrame(root)
    Notebook.add(recorder_widget.main_container, text='Recorder')

    map_widget = Map.MapFrame(root)
    Notebook.add(map_widget.main_container, text='Operational Map')
    main_panel.add(Notebook)

    root.mainloop()
