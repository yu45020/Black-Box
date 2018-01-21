import io
import tkinter as tk
from os import path
# from time import strftime
from tkinter.filedialog import askopenfilename, asksaveasfilename
from MasterFrame import MasterFrame
from PIL import ImageTk, Image

import utils

# fix_height, fix_width = 640, 960

title = "Aigis Widget Box 2.718"


# ++++++++++++++++++++++++++++++++++++++++
#          Setup
# ++++++++++++++++++++++++++++++++++++++++

# +++++++++++++  Frames +++++++++++

class MapFrame(MasterFrame):
    def __init__(self, master):
        MasterFrame.__init__(self, master=master)

        # --- Map default settings
        self.map_file_loc = ''
        self.map_img = ''
        self.map_width = self.map_width_ = 960
        self.map_height = self.map_height_ = 640
        self.map_pixel_ratio = self.map_pixel_ratio_ = 1.5
        self.map_healer_range = self.map_healer_range_ = 40

        # --- Add Instruction
        Instruction = "Double click to draw circle and right click to erase the closest circle."
        self.main_frame.bind("<Motion>", lambda x=None: self.update_status_bar_text(Instruction))

        # ---- buttons frame ---------
        self.button_frame = tk.Frame(self.main_frame, bg='white')
        self.button_frame.pack(side='top', expand=False, pady=10, fill='y')

        # -- add widgets
        self.load_map_bn = tk.Button(self.button_frame, text='Load Map', command=self.load_map)
        self.load_map_bn.pack(side='left', padx=5, fill='y')

        self.crop_bn = tk.Button(self.button_frame, text='Crop Map', command=self.crop_img_window, state=tk.DISABLED)
        self.crop_bn.pack(side='left', padx=5, fill='y')

        self.update_set_bn = tk.Button(self.button_frame, text='Update Settings', command=self.update_set_window)
        self.update_set_bn.pack(side='left', padx=5, fill='y')

        self.circle_box = tk.LabelFrame(self.button_frame)
        self.circle_box.pack(side='left', fill='y', padx=5)
        # --range label
        self.range_entry = self.create_labeled_entry(master=self.circle_box,
                                                     label_text='Range: ',
                                                     default_value=260)

        # --check healer
        healer_var = tk.IntVar()
        self.healer_check = tk.Checkbutton(self.circle_box, text='Healer', variable=healer_var)
        self.healer_check.var = healer_var
        self.healer_check.pack(side='right', fill='y', padx=5)

        self.save_map_bn = tk.Button(self.button_frame, text='Save Map', command=self.save_map)
        self.save_map_bn.pack(side='right', fill='y', padx=5)

        # -----   image frame   ------------
        self.map_frame = tk.LabelFrame(self.main_frame, background='white')
        self.map_frame.pack(side='top', expand=False, padx=10, pady=10)
        self.img_canvas = tk.Canvas(self.map_frame, width=self.map_width, height=self.map_height, background='white')
        self.img_canvas.pack(expand=False)
        self.circle_df = {"locs": [], 'index': [0]}
        # ------ binding events
        self.img_canvas.bind("<Double-Button-1>", self.draw_circles)  # double click
        self.img_canvas.bind("<Button-3>", self.del_circles)  # right click
        self.img_canvas.bind("<Motion>", lambda event: self.update_status_bar_text('(x={}, y={})'.format(event.x,
                                                                                                               event.y)))

    def draw_circles(self, event):
        r = float(self.range_entry.get()) / 2 * float(self.map_pixel_ratio)
        x, y = event.x, event.y
        self.circle_df['locs'].append([x, y])
        tag_counter = self.circle_df['index'][-1]
        tag_id = 'circle' + str(tag_counter)
        self.img_canvas.create_oval(x - 8, y - 8, x + 8, y + 8, fill='gray', tags=tag_id)
        self.img_canvas.create_oval(x - r, y - r, x + r, y + r, fill='', outline='red', tags=tag_id)

        if self.healer_check.var.get():  # if the healer is checked
            r_healer = self.map_healer_range / 2 + r
            self.img_canvas.create_oval(x - r_healer, y - r_healer, x + r_healer, y + r_healer,
                                        fill='', outline='lime', dash="--", width=0.2, tags=tag_id)
        self.circle_df['index'].append(tag_counter + 1)

    def del_circles(self, event):
        if self.circle_df['locs']:
            x, y = event.x, event.y
            distance = []
            for (x0, y0) in self.circle_df['locs']:
                dist = (x0 - x) ** 2 + (y0 - y) ** 2
                distance.append(dist)

            closest_index = distance.index(min(distance))
            closest_tag = 'circle' + str(self.circle_df['index'][closest_index])
            closest_circles = self.img_canvas.find_withtag(closest_tag)
            self.circle_df['locs'].pop(closest_index)
            self.circle_df['index'].pop(closest_index)
            for circle in closest_circles:
                self.img_canvas.delete(circle)

    def load_map(self):
        map_file = askopenfilename()
        if map_file:
            self.map_file_loc = map_file
            self.map_img, msg = utils.load_map(map_file, fix_width=self.map_width, fix_height=self.map_height)
            self.img_canvas.create_image(0, 0, image=self.map_img, anchor="nw", tags='map')
            self.update_status_bar_text(msg)
            self.crop_bn.config(state=tk.NORMAL)

    def save_map(self):
        if self.map_img:
            loc_to_save = asksaveasfilename(defaultextension=".jpg",
                                            filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")))

            if loc_to_save:
                if not loc_to_save.endswith('.png') or not loc_to_save.endswith('.jpg'):
                    loc_to_save += ".jpg"

                # Tkinter use postscript to save canvas plots
                try:  # need postscript
                    img_ps = self.img_canvas.postscript(colormode='color')
                    img = Image.open(io.BytesIO(img_ps.encode('utf-8')))
                    img.save(loc_to_save)
                    msg = 'Saved'
                except:
                    msg = 'Fail to use Ghostscript to convert postscript, so snapshot this window.'
                    utils.snap_shot(program_dict={"class_name": "TkTopLevel", "title": title}, location=loc_to_save)
                self.update_status_bar_text(msg)

    def update_set_window(self):
        def update():
            self.map_pixel_ratio = float(pixel_ratio.get())
            self.map_healer_range = float(healer_range.get())
            width, height = int(map_width.get()), int(map_height.get())
            if width != self.map_width or height != self.map_height:
                self.map_width, self.map_height = width, height
                self.img_canvas.delete('all')
                self.map_img, msg = utils.load_map(self.map_file_loc, fix_width=int(width), fix_height=int(height))
                self.img_canvas.config(height=height, width=width)
                self.img_canvas.create_image(0, 0, image=self.map_img, anchor="nw", tags='map')
                self.update_status_bar_text(msg)
            update_window.master.destroy()

        def reset():
            map_width.value.set(self.map_width_)
            map_height.value.set(self.map_height_)
            pixel_ratio.value.set(self.map_pixel_ratio_)
            healer_range.value.set(self.map_healer_range_)

        update_window = self.create_simple_dlg_window('Update Map Settings')
        update_frame = tk.LabelFrame(update_window.main_frame)
        update_frame.pack(padx=10, pady=10)
        update_window.main_frame.focus_set()  # initial focus when the window open

        # create entries into the body frame
        map_width = self.create_labeled_entry(update_frame, 'Map Width: ', self.map_width, 'top')
        map_height = self.create_labeled_entry(update_frame, 'Map Height: ', self.map_height, 'top')
        pixel_ratio = self.create_labeled_entry(update_frame, 'Pixel Ratio: ', self.map_pixel_ratio, 'top')
        healer_range = self.create_labeled_entry(update_frame, 'Healer Extra Range: ', self.map_healer_range, 'top')
        message_line = tk.Label(update_frame, text="Healer's possible range: Range * Pixel Ratio + extra range")
        message_line.pack(side='top')

        # create buttons
        button_box = tk.Label(update_window.main_frame, bg='white')
        button_box.pack(side='top', expand=False, pady=0)

        reset_bn = tk.Button(button_box, text='Reset', width=10, command=reset)
        reset_bn.pack(side='left', padx=5, fill='x')

        close_bn = tk.Button(button_box, text='Close', width=10,
                             command=lambda event=None: update_window.master.destroy())
        close_bn.pack(side='right', padx=5, fill='x', expand=False)

        update_bn = tk.Button(button_box, text='Update', width=10, command=update)
        update_bn.pack(side='right', padx=5, fill='x')

    def crop_img_window(self):
        def select_bottom_cords(event):
            right_bottom_x.value.set(event.x)
            right_bottom_y.value.set(event.y)
            if left_top_x.get():
                preview_bn.config(state=tk.NORMAL)

        def select_top_cords(event):
            left_top_x.value.set(event.x)
            left_top_y.value.set(event.y)
            if right_bottom_x.get():
                preview_bn.config(state=tk.NORMAL)

        def preview_img():
            img_ = Image.open(self.map_file_loc)
            img = img_.crop(
                (int(left_top_x.get()),
                 int(left_top_y.get()),
                 int(right_bottom_x.get()),
                 int(right_bottom_y.get())
                 )
            )
            file_path = path.dirname(self.map_file_loc)
            self.cropped_img_loc = file_path + "/cropped" + path.basename(self.map_file_loc)
            img.save(self.cropped_img_loc)
            self.crop_img_preview = ImageTk.PhotoImage(img)
            self.crop_window_img_canvas.delete('map')
            self.crop_window_img_canvas.create_image(0, 0, image=self.crop_img_preview,
                                                     anchor="nw", tags='map')
            Confirm_bn.config(state=tk.NORMAL)
            reset_bn.config(state=tk.NORMAL)

        def confirm_img():
            self.map_file_loc = self.cropped_img_loc
            self.img_canvas.create_image(0, 0, image=self.crop_img_preview, anchor="nw", tags='map')
            crop_window.master.destroy()

        intstr = 'Double click to detect left top corner and right click to detect the bottom right. ' \
                 'Cropped Img is saved in the same folder in preview.'

        crop_window = self.create_simple_dlg_window(pop_win_title=intstr)
        crop_window.master.geometry("%dx%d+0+0" % (self.max_w * 0.9, self.max_h * 0.9))

        # ------------------    Images  -----------------------------
        img_frame = tk.LabelFrame(crop_window.main_frame)
        img_frame.pack(padx=10, pady=5, fill='both', expand=True)
        img_frame.focus_set()  # initial focus when the window open

        self.crop_window_img_canvas = tk.Canvas(img_frame, background='white')
        self.crop_window_img_canvas.pack(fill='both', expand=True)
        self.crop_img = ImageTk.PhotoImage(Image.open(self.map_file_loc))
        self.crop_window_img_canvas.create_image(0, 0, image=self.crop_img, anchor="nw", tags='map')

        self.crop_window_img_canvas.bind("<Double-Button-1>", select_top_cords)  # left double click
        self.crop_window_img_canvas.bind("<Button-3>", select_bottom_cords)  # right click

        # --------------------  Buttons    -----------------------
        button_frame = tk.LabelFrame(crop_window.main_frame)

        button_frame.pack(padx=10, pady=5)

        close_bn = tk.Button(button_frame, text='Close', width=10,
                             command=lambda event=None: crop_window.master.destroy())
        close_bn.pack(side='right', padx=5, fill='x', expand=False)

        reset_bn = tk.Button(button_frame, text='Reset', state=tk.DISABLED,
                             command=lambda: self.crop_window_img_canvas.create_image(0, 0, image=self.crop_img,
                                                                                      anchor="nw", tags='map'))
        reset_bn.pack(side='right', padx=5)

        preview_bn = tk.Button(button_frame, text='Preview', state=tk.DISABLED, command=preview_img)
        preview_bn.pack(side='right', padx=5)

        Confirm_bn = tk.Button(button_frame, text='Confirm', state=tk.DISABLED,
                               command=confirm_img)
        Confirm_bn.pack(side='right', padx=5)

        # ----------        Crop Locs ----------------------------
        left = tk.Label(button_frame)
        right = tk.Label(button_frame)
        left.pack(side='left')
        right.pack(side='left')
        left_top_x = self.create_labeled_entry(left, "Left Top X", 0, side='top')
        left_top_y = self.create_labeled_entry(left, "Left Top Y", 0, side='top')
        right_bottom_x = self.create_labeled_entry(right, "Right Bottom X", 0, side='top')
        right_bottom_y = self.create_labeled_entry(right, "Right Bottom Y", 0, side='top')

    def update_status_bar_text(self, msg):
        self.status.config(text=msg)


if __name__ == "__main__":
    root = tk.Tk()
    # root.geometry("1280x750")
    root.title(title)
    app = MapFrame(root, 'Map')
    root.mainloop()
