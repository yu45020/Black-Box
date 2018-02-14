import win32api
from operator import sub

import keyboard
import pywinauto
from pywinauto.findwindows import find_windows
from pywinauto.win32functions import GetWindowRect, GetSystemMetrics

from MasterFrame import *


class HotKeyMapper(MasterFrame):
    width = GetSystemMetrics(0)
    height = GetSystemMetrics(1)

    def __init__(self, master):
        MasterFrame.__init__(self, master=master)
        # they are relative position inside the game window
        self.keymap = {"ctrl+tab": (0, 0),  # x2 speed
                       "ctrl+`": (0, 0),  # skill
                       "ctrl+1": (0, 0),
                       "ctrl+2": (0, 0),
                       "ctrl+3": (0, 0),
                       "ctrl+4": (0, 0)}
        # map absolute mouse position to client's position. Reference point:  (Left, Top)
        self.off_set = (0, 0)
        self.client = (0, 0)  # client window size (right, bottom)
        self.keymapper()
        self.initUI()
        self.app = None  # for pywinauto
        self.dlg = None  # for pywinauto

        self.connect_game()

    # +++++++++++++++++++++++++++++++++++++
    #           Set hot keys
    # -------------------------------------

    def keymapper(self):
        for ctrl_key in self.keymap.keys():
            key = ctrl_key.split('+')[1]
            # set mouse click location (ctrl+ key)
            keyboard.add_hotkey(ctrl_key, suppress=True, timeout=1,
                                callback=self.hot_key_location, args=[ctrl_key])
            # simulate click (key)
            keyboard.add_hotkey(key, suppress=True, timeout=1,
                                callback=self.hot_key_click, args=[ctrl_key])

    def hot_key_location(self, hotkey):
        cursor_loc = win32api.GetCursorPos()
        cursor_loc = tuple(map(sub, cursor_loc, self.off_set))
        print(cursor_loc)
        self.keymap[hotkey] = cursor_loc
        print(hotkey)
        print("registered")
        self.update_loc_label()

    def hot_key_click(self, hotkey):
        loc = self.keymap[hotkey]
        self.dlg.set_focus()
        self.dlg.click(button='left', coords=loc, double=True)
        print("clicked")

    # +++++++++++++++++++++++++++++++++++++
    #           Connect game by window title
    # -------------------------------------

    def connect_game(self):
        game_title = self.game_title_entry.get()
        handle = find_windows(title_re=game_title)
        if handle:
            # connect to the game handle
            self.app = pywinauto.Application().connect(handle=handle[0])
            self.dlg = self.app.window()
            self.status.config(text="Connected.")
            print("connected")
            self.update_key_locations()
            self.update_loc_label()

        else:
            self.status.config(text="Can't find the window.")

    def update_key_locations(self):
        # calculate offset and reset 2 hotkeys location
        client_in_window = self.dlg.get_properties()['rectangle']
        self.off_set = (client_in_window.left, client_in_window.top)
        client = self.dlg.get_properties()['client_rects'][0]
        # x2
        self.keymap['ctrl+tab'] = (client.right - 50, 50)
        # skill
        self.keymap['ctrl+`'] = (client.right - 50, client.bottom - 50)
        if self.client != (client.right, client.bottom):  # if scaled larger/smaller
            self.client = (client.right, client.bottom)
            rest_keys = ["ctrl+" + str(x) for x in range(1, 5)]
            for key in rest_keys:  # reset unit locations to 0
                self.keymap[key] = (0, 0)

    # +++++++++++++++++++++++++++++++++++++
    #           Boring UI
    # -------------------------------------

    def initUI(self):

        game_name_frame = tk.LabelFrame(self.main_frame)
        game_name_frame.pack()

        self.reconize_file = ''
        self.connect = tk.Button(game_name_frame, text='Connect Game', command=self.connect_game)
        self.connect.pack(side='top', padx=5, pady=5)
        self.game_title_value = tk.StringVar()
        self.game_title_value.set('千年戦争アイギス')  # 千年戦争アイギス  AigisPlayer
        self.game_title_entry = tk.Entry(game_name_frame, textvariable=self.game_title_value)
        self.game_title_entry.pack(side='top', padx=5, pady=5)

        hotkey_inst = tk.Label(self.main_frame, justify=tk.LEFT,
                               width=30, height=2,
                               text="ctrl + tab,`, 1 ... : 记录鼠标位置 \n tab, `, 1 ...       :  模拟鼠标双击")
        hotkey_inst.pack(side='top', padx=5, pady=5)

        hotkey_map_frame = tk.LabelFrame(self.main_frame, width=30)
        hotkey_map_frame.pack(side='top', padx=5, pady=5)

        self.hotkey_00 = tk.Label(hotkey_map_frame, width=30, text='x2 ctrl+tab:   {}'.format(self.keymap['ctrl+tab']),
                                  justify=tk.LEFT)
        self.hotkey_0 = tk.Label(hotkey_map_frame, width=30, text='技能 ctrl+`:     {}'.format(self.keymap["ctrl+`"]),
                                 justify=tk.LEFT)
        self.hotkey_1 = tk.Label(hotkey_map_frame, width=30, text='单位 ctrl+1:     {}'.format(self.keymap["ctrl+1"]),
                                 justify=tk.LEFT)
        self.hotkey_2 = tk.Label(hotkey_map_frame, width=30, text='单位 ctrl+2:     {}'.format(self.keymap["ctrl+2"]),
                                 justify=tk.LEFT)
        self.hotkey_3 = tk.Label(hotkey_map_frame, width=30, text='单位 ctrl+3:     {}'.format(self.keymap["ctrl+3"]),
                                 justify=tk.LEFT)
        self.hotkey_4 = tk.Label(hotkey_map_frame, width=30, text='单位 ctrl+4:     {}'.format(self.keymap["ctrl+4"]),
                                 justify=tk.LEFT)
        self.hotkey_00.pack(anchor="nw")
        self.hotkey_0.pack(anchor="nw")
        self.hotkey_1.pack(anchor="nw")
        self.hotkey_2.pack(anchor="nw")
        self.hotkey_3.pack(anchor="nw")
        self.hotkey_4.pack(anchor="nw")

    def update_loc_label(self):
        self.hotkey_00.config(text='重置 x2 tab:        {}'.format(self.keymap['ctrl+tab']))
        self.hotkey_0.config(text='重置技能 ctrl+`:     {}'.format(self.keymap["ctrl+`"]))
        self.hotkey_1.config(text='重置单位 ctrl+1:     {}'.format(self.keymap["ctrl+1"]))
        self.hotkey_2.config(text='重置单位 ctrl+2:     {}'.format(self.keymap["ctrl+2"]))
        self.hotkey_3.config(text='重置单位 ctrl+3:     {}'.format(self.keymap["ctrl+3"]))
        self.hotkey_4.config(text='重置单位 ctrl+4:     {}'.format(self.keymap["ctrl+4"]))


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('320x350')
    root.title("热键映射")
    app = HotKeyMapper(root)
    root.mainloop()

