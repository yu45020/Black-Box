from os import path, environ
import io
import tkinter as tk
from time import strftime
from tkinter.filedialog import askopenfilename, askdirectory, asksaveasfilename
from PIL import Image, ImageTk, ImageGrab
import utils

title = "Aigis Widget Box 2.718"

class MasterFrame:
    def __init__(self, master, frame_title=None):
        self.master = master
        self.main_container = tk.Frame(master)
        self.main_container.pack(side='top', expand=True, fill='both')

        # ---- make subtitle
        self.title_frame = tk.Frame(self.main_container)
        self.title_frame.pack(side='top', expand=False, fill='x')
        self.title_label = tk.Label(self.title_frame, text=frame_title)
        self.title_label.pack(side='top', expand=False)

        # ---- body frame
        self.main_frame = tk.Frame(self.main_container, bg='white')
        self.main_frame.pack(side='top', fill='both', expand=True)

        # ---- status bar
        self.status_bar = tk.Frame(self.main_container)
        self.status_bar.pack(side='bottom', fill='both', expand=False)
        self.status = tk.Label(self.status_bar)
        self.status.pack(side='bottom', fill='x', expand=False)

    def create_simple_dlg_window(self, pop_win_title):
        # return the top window
        pop_window = tk.Toplevel(self.master)
        pop_window.title(pop_win_title)
        pop_window.transient(self.master)
        pop_window.grab_set()  # grab focus and pop up window size
        pop_window.geometry("+%d+%d" % (self.master.winfo_rootx() + 50, self.master.winfo_rooty() + 50))
        return pop_window

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

class MainPalen(MasterFrame):
    def __init__(self, master, frame_title):
        MasterFrame.__init__(self, master=master, frame_title=frame_title)


if __name__ == "__main__":
    root = tk.Tk()
    # root.geometry("1280x750")
    root.title(title)

    app = MainPalen(root, 'Main Panel')
    root.mainloop()

