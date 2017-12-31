from AutoClick import *
import time

runtime = 60*2  # seconds
icon = "click1.jpg"

program = AutoClick(program_title="あい", ImgPath='airisu_img')
#  Screen shot the background image
program.screen_shot()
screen_w, screen_h = program.screen_img.shape[::-1]

#  Detect Icon location (x, y)
icon_loc = program.detect_icon_loc(icon, enlarge_icon=False)
icon_w, icon_h = cv2.imread(program.ImgPath + icon, 0).shape[::-1]

#  Note, all 3 click points have the same ratio: (0.486, 0.572, 0.863)
#  Please check the screen shot in the folder

click_point2 = (int(0.486 * screen_w), icon_loc[1])
program.locs.append(click_point2)

click_point3 = (int(0.572 * screen_w), icon_loc[1])
program.locs.append(click_point3)

timeout = time.time() + runtime
while program.dlg.is_normal():
    for loc in program.locs:
        program.click(loc)

    if time.time() > timeout:
        break


#   Test
# ++++++++++++++++++++++++++++++++++
# import matplotlib.pyplot as plt
# plt.imshow(program.screen_img, cmap='gray')
# p lt.plot(program.locs[0][0], program.locs[0][1], marker='o')
# program.dlg.move_mouse(icon_loc)
# 430 / 862, 534 / 862, 765 / 862
# 578 / 1188, 680 / 1188, 1027 / 1188
# ++++++++++++++++++++++++++++++++++
