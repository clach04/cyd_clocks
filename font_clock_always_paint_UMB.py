# font_clock_always_paint.py
"""Micropython Clock that paints every time it gets a chance, so as to measure FPS
Uses on-disk font.

3-4FPS with UbuntuMonoBold29x42numbers (48) - font would be better if a little larger for clock
0-1FPS with UbuntuMonoBold43x61numbers.c (72) - font size JUST fits screen width - TODO some slight corruption where old pixels left around on repaint. Also not the best font
framerate unstable, needs accurate sleep (rather than whole secs)

TODO use a (pre-processed) pure code font, rather than parsing C code at runtime.
TODO perform math to calculate sub-second sleep time, rather than always sleeping for 1 second.
"""

import machine
import time

#from machine import Pin, SPI  # TODO style decision
from ili9341 import Display, color565  # from https://github.com/rdagger/micropython-ili9341
from xglcd_font import XglcdFont


# Baud rate of 40000000 seems about the max
spi = machine.SPI(1, baudrate=40000000, sck=machine.Pin(14), mosi=machine.Pin(13))
# display = Display(spi, dc=Pin(4), cs=Pin(16), rst=Pin(17))
# TODO see if can use lvgl API, which has different parameters
# bgr-mode disabled for CYD2
display = Display(
            spi, dc=machine.Pin(2), cs=machine.Pin(15),
            rst=machine.Pin(15),
            width=320, height=240,  # ommit this and endup with square, with static on right hand side
            bgr=False,
            gamma=False
)

backlight = machine.Pin(21, machine.Pin.OUT)
backlight.on()  # TODO review PWM instead of on/off

# NOTE expects local time set (via Thonny) for now

# setup functions for time, note this is both for API (readability) but it also massively impacts performance by reducing module lookup (almost 50fps with simple clock)
#timer_function = utime.time
timer_function = time.time

#local_time_tuple_function = utime.localtime
local_time_tuple_function = time.localtime  # NOTE **not** a struct under micropython!

COLOR_WHITE = color565(255, 255, 255)
COLOR_BLACK = color565(0, 0, 0)

def display_clock():
    bg_color = COLOR_WHITE
    fg_color = COLOR_BLACK
    x, y = 0, 0
    #fps_x, fps_y = 100, 100
    #fps_x, fps_y = 0, 240 - 8
    fps_x, fps_y = 250, 240 - 8

    start_time = timer_function()
    fps_counter = 0

    # load font. NOTE this is expensive/slow
    #unispace = XglcdFont('fonts/umb31x57_numbers.c', 31, 57)  # entire us-ascii set causes; MemoryError: memory allocation failed, allocating 23904 bytes
    #unispace = XglcdFont('fonts/umb31x57_numbers.c', 29, 42, start_letter=48, letter_count=11)  # size 48 font import Ubuntu Mono Bold
    unispace = XglcdFont('fonts/UbuntuMonoBold43x61numbers.c', 43, 61, start_letter=48, letter_count=11)  # Ubuntu Mono Bold size 72 font import
    xpos = 0
    ypos = 0

    while True:
        l = local_time_tuple_function()
        time_str = '%02d:%02d:%02d' % (l[3], l[4], l[5])
        display.draw_text(xpos, ypos + 100, time_str, unispace, COLOR_WHITE)  # FIXME this does not clear existing written text, need to clear for clean output

        # simple FPS math. Consider implementing a clone of pygame.time.Clock() which has a tick()/get_fps() interface https://www.pygame.org/docs/ref/time.html#pygame.time.Clock.get_fps - below is probably faster?
        # Also see lvgl macro define LV_USE_PERF_MONITOR
        fps_counter += 1
        if (timer_function() - start_time) > 1:  # calc every 1 (one) second
            fps = fps_counter / (timer_function() - start_time)  # NOTE faster to call again than to store and use local variable
            #fps_str = "FPS: %f" % (fps,)
            fps_str = "FPS: %d" % (int(fps),)
            #print(fps_str)  # to serial
            display.draw_text8x8(fps_x, fps_y, fps_str, COLOR_WHITE, COLOR_BLACK)
            fps_counter = 0  # reset
            start_time = timer_function()


try:
    display_clock()
finally:
    display.cleanup()  # OSError: transfer on deinitialized SPI -- suspect still need spi here
    spi.deinit()
    backlight.off()
