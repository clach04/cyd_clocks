# tiny_8x8_clock_always_paint_framebuf.py
"""Micropython Clock that uses an internal framebuffer and paints every time it gets a chance, so as to measure FPS

~ 450fps for dumb small text font

https://docs.micropython.org/en/latest/library/framebuf.html

https://github.com/witnessmenow/ESP32-Cheap-Yellow-Display/blob/main/Examples/Micropython/Micropython.md

"""

from framebuf import FrameBuffer, RGB565  # https://docs.micropython.org/en/latest/library/framebuf.html
import machine
#from machine import Pin, SPI  # TODO style decision
import time
#import utime  # docs recommend against this, as likely to go away
#from utime import sleep, localtime

from ili9341 import Display, color565  # from https://github.com/rdagger/micropython-ili9341 (potentially modified version from https://github.com/de-dh/ESP32-Cheap-Yellow-Display-Micropython-LVGL/tree/main/demo_no_lvgl)


width = 320
height = 240

# Baud rate of 40000000 seems about the max
spi = machine.SPI(1, baudrate=40000000, sck=machine.Pin(14), mosi=machine.Pin(13))
# display = Display(spi, dc=Pin(4), cs=Pin(16), rst=Pin(17))
# TODO see if can use lvgl API, which has different parameters
# bgr-mode disabled for CYD2
display = Display(
            spi, dc=machine.Pin(2), cs=machine.Pin(15),
            rst=machine.Pin(15),
            width=width, height=height,  # ommit this and endup with square, with static on right hand side
            bgr=False, gamma=True
)

backlight = machine.Pin(21, machine.Pin.OUT)
backlight.on()  # TODO review PWM instead of on/off


"""
# FrameBuffer needs 2 bytes for every RGB565 pixel
fbuf_bytearray = bytearray(width * height * 2)  # MemoryError: memory allocation failed, allocating 153600 bytes  -- gc.mem_free(); == 79056
fbuf = FrameBuffer(fbuf_bytearray, width, height, RGB565)
"""
# FrameBuffer needs 2 bytes for every RGB565 pixel
fb_width = 100  # can not have a full screen (doubler) buffer :-(
fb_height = 100
print('pre-buf alloc') ; time.sleep(2)
fbuf_bytearray = bytearray(fb_width * fb_height * 2)  # MemoryError: memory allocation failed, allocating 153600 bytes  -- gc.mem_free(); == 79056
print('post-buf alloc') ; time.sleep(2)
fbuf = FrameBuffer(fbuf_bytearray, width, height, RGB565)
print('pre-buf fill') ; time.sleep(2)
#fbuf.fill(0)  # casuses Guru Meditation Error: Core  1 panic'ed (LoadStoreError). Exception was unhandled.
print('post-buf fill') ; time.sleep(2)

# NOTE expects local time set (via Thonny) for now

# setup functions for time, note this is both for API (readability) but it also massively impacts performance by reducing module lookup (almost 50fps with simple clock)
timer_function = time.time
local_time_tuple_function = time.localtime  # NOTE **not** a struct under micropython!

COLOR_WHITE = color565(255, 255, 255)
COLOR_BLACK = color565(0, 0, 0)


def display_clock():
    bg_color = 1
    fg_color = 1
    x, y = 0, 0
    #fps_x, fps_y = 100, 100
    #fps_x, fps_y = 0, 240 - 8
    #fps_x, fps_y = 250, 240 - 8
    #fps_x, fps_y = 50, fb_height - 8  # reduced for framebuffer
    fps_x, fps_y = 50, fb_height - 8  # reduced for framebuffer

    start_time = timer_function()
    fps_counter = 0

    while True:
        print('pre-get time') ; time.sleep(2)
        l = local_time_tuple_function()
        time_str = '%02d:%02d:%02d' % (l[3], l[4], l[5])
        time_str = 'T'  # DEBUG
        print('pre-date')
        date_str = '%04d-%02d-%02d' % (l[0], l[1], l[2])  # with this present BUT not the display, ~420 fps (down from ~450 without)
        date_str = 'D'  # DEBUG
        print('pre-draw text 1')
        time.sleep(2)
        fbuf.text(time_str, x, y, fg_color)
        print('pre-draw text 2')
        #fbuf.text(date_str, 0, fps_y, fg_color)  # with this present, ~237 fps (down from ~450 without)
        print('post-draw text 2')

        # simple FPS math. Consider implementing a clone of pygame.time.Clock() which has a tick()/get_fps() interface https://www.pygame.org/docs/ref/time.html#pygame.time.Clock.get_fps - below is probably faster?
        # Also see lvgl macro define LV_USE_PERF_MONITOR
        fps_counter += 1
        if (timer_function() - start_time) > 1:  # calc every 1 (one) second
            fps = fps_counter / (timer_function() - start_time)  # NOTE faster to call again than to store and use local variable
            #fps_str = "FPS: %f" % (fps,)
            fps_str = "FPS: %d" % (int(fps),)
            fps_str = 'F'  # DEBUG
            #print(fps_str)  # to serial
            print('pre-draw text 3'); time.sleep(2)
            fbuf.text(fps_str, fps_x, fps_y, bg_color)  # Guru Meditation Error: Core  1 panic'ed (LoadStoreError). Exception was unhandled.
            print('post-draw text 3'); time.sleep(2)
            fps_counter = 0  # reset
            start_time = timer_function()

        print('pre-draw sprite')
        #display.draw_sprite(fbuf, 0, 0, fb_width, fb_height)  # review for fps timing / measurement

try:
    print('pre-display_clock') ; time.sleep(2)
    display_clock()
finally:
    display.cleanup()
    spi.deinit()
    backlight.off()

