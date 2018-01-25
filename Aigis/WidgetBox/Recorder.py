import tkinter as tk
import os
import cv2
from time import strftime
import numpy as np
import utils
from MasterFrame import MasterFrame
from PIL import Image, ImageTk


class RecorderFrame(MasterFrame):
    def __init__(self, master):
        MasterFrame.__init__(self, master=master)

        snapshot_frame = tk.LabelFrame(self.main_frame)
        snapshot_frame.pack()

        self.reconize_file = ''
        self.snapshot_bn = tk.Button(snapshot_frame, text='Snapshot', command=self.snapshot)
        self.snapshot_bn.pack(side='left', padx=5)

        self.game_title_value = tk.StringVar()
        self.game_title_value.set('AigisPlayer')  # 千年戦争アイギス
        self.game_title_entry = tk.Entry(snapshot_frame, textvariable=self.game_title_value)
        self.game_title_entry.pack(side='left', padx=5)

        self.snapshot_res = tk.Label(snapshot_frame)
        self.snapshot_res.pack(side='right', padx=5)

        self.store_loc = './Drop_Record/'
        if not os.path.isdir(self.store_loc):
            os.mkdir(self.store_loc)

        self.detect_bn = tk.Button(self.main_frame, text='Detect Items', command=self.detect_items)
        self.detect_bn.pack(padx=5, pady=5)
        self.detect_label = tk.LabelFrame(self.main_frame, text='Result')
        self.detect_label.pack(padx=5, pady=5)

        self.detect_res_canvas = tk.Canvas(self.detect_label, width=60, height=60)
        icon = Image.open(self.store_loc + "gold.jpg")
        icon = icon.resize((50, 50))
        self.glod_icon = ImageTk.PhotoImage(icon)
        self.detect_res_canvas.create_image(0, 0, image=self.glod_icon, anchor="nw", tags='icon')
        self.detect_res_canvas.pack(side='left')

        self.detect_res = tk.Label(self.detect_label)
        self.detect_res.pack(padx=5, pady=5)

        self.detect_res = tk.Label(self.detect_label)
        self.detect_res.pack(padx=5, pady=5)

    def snapshot(self):
        try:
            self.reconize_file = self.store_loc + strftime("%Y%m%d_%H%M%S") + '.jpg'
            utils.snap_shot(program_dict={"title_re": self.game_title_entry.get()}, location=self.reconize_file)
            msg = 'Success'
        except:
            msg = "Failed"
        self.snapshot_res.config(text=msg)

    def detect_items(self):
        self.snapshot()
        img = cv2.imread(self.reconize_file, 0)
        # img = img.crop((185,478,811,574))
        img = img[658:870, 234:900]  # y:y+h, x:x+w
        temp = cv2.imread(self.store_loc + "gold.jpg", 0)
        res = cv2.matchTemplate(image=img, templ=temp, method=cv2.TM_CCOEFF_NORMED)
        tehreshold = 0.95
        loc = np.where(res >= tehreshold)
        self.detect_res.config(text=len(loc[0]))



if __name__ == "__main__":
    img = cv2.imread("./Drop_Record/test1.jpg", 0)
    temp = cv2.imread("./Drop_Record/gold.jpg", 0)
    res = cv2.matchTemplate(image=img, templ=temp, method=cv2.TM_CCOEFF_NORMED)
    tehreshold = 0.95
    loc = np.where(res >= tehreshold)
    len(loc[0])

    w, h = img.shape[::-1]
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        cv2.imwrite('res.png', img)
