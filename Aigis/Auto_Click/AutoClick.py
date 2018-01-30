import cv2
import pywinauto
from pywinauto.findwindows import find_windows
import sys
import numpy as np
import os
from win32api import GetSystemMetrics


class AutoClick:
    screen_w = GetSystemMetrics(0)
    screen_h = GetSystemMetrics(1)

    def __init__(self, program_title=None, program_exe=None, ImgPath='img'):
        """
        :param program_title: title name of a window (partial is OK)
        :param program_exe: path to a program
        """
        if program_exe is not None:
            app = pywinauto.Application().start(program_exe)  # start the program

        elif program_title is not None:  # get the program id and connect to it
            handle = find_windows(title_re=program_title)[0]
            app = pywinauto.Application().connect(handle=handle)

        else:
            print("Please input program_title or program_exe")
            sys.exit()

        if not os.path.exists(ImgPath):
                os.makedirs(ImgPath)

        self.ImgPath = './' + ImgPath + '/'

        self.dlg = app.window()  # get the window of the program (assume there is only one)
        self.locs = []  # list of locations to click; order matters
        self.ratio = 1  #ratio to enlarge/shrink icon

    def screen_shot(self):
        img = self.dlg.capture_as_image()
        self.screen_name = "screen_shot.jpg" 
        img.save(self.screen_name)
        self.screen_img = cv2.imread(self.screen_name, 0)  # load image in gray scale

    def detect_icon_loc(self, icon_file, loc_confidence=0.8, enlarge_icon=False):
        icon_temp = cv2.imread(self.ImgPath + icon_file, 0)
        icon_w, icon_h = icon_temp.shape[::-1]

        res = cv2.matchTemplate(image=self.screen_img, templ=icon_temp,
                                method=cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        optimal_loc = min_loc[0] + int(icon_w/2), min_loc[1] + int(icon_h/2)
        best_loc = [1 - min_val, optimal_loc]

        if best_loc[0] < loc_confidence and enlarge_icon:
            # enlarge icon by many scales and return the optimal result
            best_loc = self.enlarge_icon_to_loc(icon_temp)
            if best_loc[0] < loc_confidence:
                return False

        self.locs.append(best_loc[1])
        print("load icon:{} and record location, and confidence {}".format(icon_file, best_loc[0]))
        return best_loc[1]

    def enlarge_icon_to_loc(self, icon_temp):
        img_w, img_h = self.screen_img.shape[::-1]

        best_loc = [0, (0, 0)]  # confidence, optimal_loc(x,y)
        ratio = np.linspace(start=1.1, stop=4, num=40)
        for r in ratio:  # loop to enlarge the icon and find the best location
            icon_temp_new = cv2.resize(icon_temp, None, fx=r, fy=r, interpolation=cv2.INTER_CUBIC)
            icon_w, icon_h = icon_temp_new.shape[::-1]

            if icon_w > img_w or icon_h > img_h:
                break

            res = cv2.matchTemplate(image=self.screen_img, templ=icon_temp_new, method=cv2.TM_SQDIFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            if (1 - min_val) > best_loc[0]:
                optimal_loc = min_loc[0] + int(icon_w / 2), min_loc[1] + int(icon_h / 2)
                best_loc = [1 - min_val, optimal_loc]
                self.ratio = r  # store the best ratio

        return best_loc

    def set_window_size(self, width, height):
        self.dlg.move_window(x=self.screen_w - width, y=0, width=width, height=height)

    def get_win_size_width(self):
        width = self.dlg.rectangle().width()
        height = self.dlg.rectangle().height()
        # x = self.dlg.rectangle().left
        # y = self.dlg.rectangle().top
        return {"width": width, "height": height}

    def click(self, loc):
        self.dlg.click_input(coords=loc)

    def simulate_click(self, loc):
        self.dlg.set_focus()
        self.dlg.click(coords=loc, double=True)

    def drag_mouse(self, press_coord, release_coord):
        self.dlg.drag_mouse_input(src=press_coord, dst=release_coord, absolute=False)

    def simulate_drag_mouse(self, press_coord, release_coord):
        self.dlg.set_focus()
        self.dlg.drag_mouse(press_coord=press_coord, release_coord=release_coord)

    @staticmethod
    def write_setting(file_name, setting):
        return np.save(file_name, setting)

    @staticmethod
    def load_setting(file_name):
        setting = np.load(file_name)
        if isinstance(setting, dict):
            setting = setting.items()
        return setting
