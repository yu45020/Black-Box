from time import strftime, sleep
from os import path
import pywinauto
from PIL import Image, ImageTk, ImageOps
from pywinauto.findwindows import find_windows
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


class MasterFrame:

    def __init__(self, master):
        self.master = master

        self.max_w = master.winfo_screenwidth()
        self.max_h = master.winfo_screenheight()

        self.main_container = tk.Frame(master)
        self.main_container.pack(side='top', expand=True, fill='both')

        # ---- make subtitle
        self.title_frame = tk.Frame(self.main_container)
        self.title_frame.pack(side='top', expand=False, fill='x')
        # self.title_label = tk.Label(self.title_frame, text=frame_title)
        # self.title_label.pack(side='top', expand=False)

        # ---- body frame
        self.main_frame = tk.Frame(self.main_container, bg='white')
        self.main_frame.pack(side='top', fill='both', expand=True)

        # ---- status bar
        self.status_bar = tk.Frame(self.main_container)
        self.status_bar.pack(side='bottom', fill='both', expand=False)
        self.status = tk.Label(self.status_bar)
        self.status.pack(side='bottom', fill='x', expand=False)

    def create_simple_dlg_window(self, pop_win_title):
        # return the top window's master frame
        pop_window = tk.Toplevel(self.master)
        pop_window.transient(self.master)
        pop_window.grab_set()  # grab focus and pop up window size
        pop_window.geometry("+%d+%d" % (self.master.winfo_rootx() + 50, self.master.winfo_rooty() + 50))

        pop_window_frame = MasterFrame(pop_window, frame_title=pop_win_title)
        return pop_window_frame

    @staticmethod
    def create_labeled_entry(master, label_text, default_value, side='left'):
        # and return entry
        label_frame = tk.Label(master)
        label_frame.pack(side=side, fill='x', padx=5)
        label = tk.Label(label_frame, text=label_text, padx=5)
        label.pack(side='left', fill='x', padx=5)

        value = tk.IntVar()
        value.set(default_value)
        entry = tk.Entry(label_frame, textvariable=value)
        entry.pack(side='right', fill="x")
        entry.value = value
        return entry


def snap_shot(program_dict, location):
    handle = find_windows(**program_dict)[0]
    if handle:
        app = pywinauto.Application().connect(handle=handle)
        dlg = app.window()
        dlg.set_focus()
        sleep(0.2)
        img = dlg.capture_as_image()
        img_name = location
        if not img_name:
            img_name = location + strftime("%Y%m%d_%H%M%S") + '.jpg'
        img.save(img_name)


def load_map(img_file, fix_height, fix_width):
    img = Image.open(img_file)
    width_img, height_img = img.size
    msg = ''
    # resize image if necessary
    if (height_img, width_img) != (fix_height, fix_width):
        img = img.resize((fix_width, fix_height), Image.BICUBIC)
        # img.save(map)

        msg = "Map is resized to (W: {}, H:{})".format(fix_width, fix_height)

    return ImageTk.PhotoImage(img), msg


def crop_img(img, left, upper, right, lower):
    return img.crop(box=(left, upper, right, lower))
