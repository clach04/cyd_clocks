# tiny_8x8_clock_always_paint.py
"""Micropython Clock that paints every time it gets a chance, so as to measure FPS

~ 450fps for dumb small text font - no date? with lvgl old MicroPython build?
# CPU clock frequency is adjustable from 80 MHz to 240 MHz
ESP32 generic - MicroPython v1.24.1 on 2024-11-29; Generic ESP32 module with ESP32
 98 FPS with 80Mhz - machine.freq(160000000)
125 FPS with 160Mhz - machine.freq(160000000)
137 FPS with 240Mhz - machine.freq(240000000)

https://github.com/witnessmenow/ESP32-Cheap-Yellow-Display/blob/main/Examples/Micropython/Micropython.md

"""

import machine
#machine.freq(80000000)
#from machine import Pin, SPI  # TODO style decision
import time
#import utime  # docs recommend against this, as likely to go away
#from utime import sleep, localtime

from ili9341 import Display, color565  # from https://github.com/rdagger/micropython-ili9341 (potentially modified version from https://github.com/de-dh/ESP32-Cheap-Yellow-Display-Micropython-LVGL/tree/main/demo_no_lvgl)


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
            gamma=False  # improves color on my CYD2 device
)

backlight = machine.Pin(21, machine.Pin.OUT)
backlight.on()  # TODO review PWM instead of on/off

# NOTE expects local time set (via Thonny) for now

# setup functions for time, note this is both for API (readability) but it also massively impacts performance by reducing module lookup (almost 50fps with simple clock)
timer_function = time.time
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

    while True:
        l = local_time_tuple_function()
        time_str = '%02d:%02d:%02d' % (l[3], l[4], l[5])
        date_str = '%04d-%02d-%02d' % (l[0], l[1], l[2])  # with this present BUT not the display, ~420 fps (down from ~450 without)
        display.draw_text8x8(x, y, time_str, fg_color, bg_color)
        display.draw_text8x8(0, fps_y, date_str, COLOR_WHITE, COLOR_BLACK)  # with this present, ~237 fps (down from ~450 without)

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
    display.cleanup()
    spi.deinit()
    backlight.off()
