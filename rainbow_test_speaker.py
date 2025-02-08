# rainbow-test.py
# Sanity check rotation and colors

import time

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
        display.fill_rectangle(offset, 0, bar_width, bar_height, color)  # (0, 0) is top left, (320, 240) is bottom right
        offset += bar_width

    #cyd.backlight_pwm.duty(1023)  # 100%
    #cyd.backlight_pwm.duty(512)  # 50%

    print('Done')  # to serial port


cyd = cyd_wrap.CYD()  # takes defaults, assumes CYD2 with 2 usb ports
try:
    display_function()

    duration = 500  # How long to play each note. (in milliseconds)
    pause = 2.0  # How long to pause in between each tone. (in seconds)

    # Play tone 1
    print("Playing Tone 1")

    cyd.play_tone(220, duration)  # A4 Tone
    time.sleep(pause)

    # Play tone 2
    print("Playing Tone 2")

    cyd.play_tone(440, duration)  # C5 Tone
    time.sleep(pause)

finally:
    # Leave screen alone/on for visual inspection - uncomment below to change that
    #cyd.cleanup()
    pass
