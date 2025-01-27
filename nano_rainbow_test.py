# nano_rainbow_test.py for use with https://github.com/peterhinch/micropython-nano-gui/
# Sanity check rotation and colors

from color_setup import ssd  # Create a display instance
from color_setup import width as WIDTH, height as HEIGHT
from gui.core.colors import create_color, RED, YELLOW, GREEN, BLUE, MAGENTA as PURPLE, WHITE, BLACK
from gui.core.nanogui import refresh


ORANGE = create_color(12, 255,128,0)


def display_function():
    refresh(ssd, True)  # Initialise and clear display.

    #color_list = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, WHITE, BLACK]
    color_list = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, WHITE]

    # generate vertical bars
    bar_width = int(WIDTH / len(color_list))
    bar_height = HEIGHT

    offset = 0
    for color in color_list:
        #FrameBuffer.rect(x, y, w, h, c[, f])¶
        ssd.rect(offset, 0, bar_width, bar_height, color, True)  # Red square at top left
        offset += bar_width
    refresh(ssd)

    print('Done')  # to serial port


try:
    display_function()
finally:
    # Leave screen alone/on for visual inspection - uncomment below to change that
    pass
