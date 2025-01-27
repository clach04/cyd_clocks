# rainbow-test.py
# Sanity check rotation and colors

import cyd_wrap
from cyd_wrap import color565, WIDTH, HEIGHT


RED = color565(255,0,0)
ORANGE = color565(255,128,0)  # if this looks brown, check cyd_wrap; bgr and gamma
YELLOW = color565(255,255,0)
GREEN = color565(0,255,0)
BLUE = color565(0,0,255)
PURPLE = color565(255,0,255)
WHITE = color565(255,255,255)
BLACK = color565(0,0,0)


def display_function():
    display = cyd.display
    display.clear()

    #color_list = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, WHITE, BLACK]
    color_list = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, WHITE]

    # generate vertical bars
    bar_width = int(WIDTH / len(color_list))
    bar_height = HEIGHT

    offset = 0
    for color in color_list:
        display.fill_rectangle(offset, 0, bar_width, bar_height, color)
        offset += bar_width

    print('Done')  # to serial port


cyd = cyd_wrap.CYD()  # takes defaults, assumes CYD2 with 2 usb ports
try:
    display_function()
finally:
    # Leave screen alone/on for visual inspection - uncomment below to change that
    #cyd.cleanup()
    pass
