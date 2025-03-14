# font_clock_rtc.py
"""Micropython Clock - uses real time clock for alarm. Untested, the micropython (hardware?) I have is missing rtc.irq, rtc.alarm , and ALARM0
Uses on-disk font.

NOTE potential for inaccuracy of a few seconds...

0-1FPS with UbuntuMonoBold43x61numbers.c (72) - font size JUST fits screen width - TODO some slight corruption where old pixels left around on repaint. Also not the best font

Uses a (pre-processed) pure code font, rather than parsing C code at runtime. Hopefully faster, hopefully more memory efficient
TODO perform math to calculate sub-second sleep time (see RTC.alarm), rather than using a Timer.
TODO look at async / uasyncio

  * https://docs.micropython.org/en/latest/esp32/quickref.html#timers
      * https://docs.micropython.org/en/latest/library/esp32.html
  * https://docs.micropython.org/en/latest/library/machine.Timer.html
  * https://docs.micropython.org/en/latest/library/machine.html#machine.idle
  * https://docs.micropython.org/en/latest/library/asyncio.html / https://docs.micropython.org/en/v1.14/library/uasyncio.html
      * https://github.com/peterhinch/micropython-async/blob/master/v3/docs/SCHEDULE.md
  * https://docs.micropython.org/en/latest/library/time.html
  * https://docs.micropython.org/en/latest/library/micropython.html#micropython.schedule
  * https://docs.micropython.org/en/latest/library/machine.RTC.html
  * https://docs.micropython.org/en/latest/library/_thread.html

3rd party

  * https://github.com/peterhinch/micropython-async/blob/master/v3/docs/SCHEDULE.md
      * https://github.com/peterhinch/micropython-async/tree/master/v3/as_drivers/sched
  * https://github.com/rguillon/schedule - MicroPython port of https://github.com/dbader/schedule
      * See ignore seconds display support:

            schedule.every(1).minutes.do(job)
            schedule.every().minute

"""

import machine
import time

#from machine import Pin, SPI  # TODO style decision
from ili9341 import Display, color565  # from https://github.com/rdagger/micropython-ili9341

import cyd_wrap
from cyd_wrap import color565, WIDTH, HEIGHT

from umb43x61numbers import UMB  # load font. hopefully faster/cheaper than XglcdFont() load


cyd = cyd_wrap.CYD()  # takes defaults, assumes CYD2 with 2 usb ports
display = cyd.display

# NOTE expects local time set (via Thonny) for now

# setup functions for time, note this is both for API (readability) but it also massively impacts performance by reducing module lookup (almost 50fps with simple clock)
#timer_function = utime.time
timer_function = time.time

#local_time_tuple_function = utime.localtime
local_time_tuple_function = time.localtime  # NOTE **not** a struct under micropython!

COLOR_WHITE = color565(255, 255, 255)
COLOR_BLACK = color565(0, 0, 0)

fps_counter = 0
start_time = timer_function()
def display_clock():
    bg_color = COLOR_WHITE
    fg_color = COLOR_BLACK
    x, y = 0, 0
    #fps_x, fps_y = 100, 100
    #fps_x, fps_y = 0, 240 - 8
    fps_x, fps_y = 250, 240 - 8


    #umb = UMB('fonts/UbuntuMonoBold43x61numbers.c', 43, 61, start_letter=48, letter_count=11)  # Ubuntu Mono Bold size 72 font import
    umb = UMB()  # Ubuntu Mono Bold size 72 font import - no params, as params ignored
    xpos = 0
    ypos = 0

    def paint_time():  # TODO should micropython.schedule() be used?
        global fps_counter
        global start_time

        l = local_time_tuple_function()
        time_str = '%02d:%02d:%02d' % (l[3], l[4], l[5])
        display.draw_text(xpos, ypos + 100, time_str, umb, COLOR_WHITE)  # FIXME this does not clear existing written text, need to clear for clean output

        # TODO add code to record/display how long a frame takes to paint

        # simple FPS math. Consider implementing a clone of pygame.time.Clock() which has a tick()/get_fps() interface https://www.pygame.org/docs/ref/time.html#pygame.time.Clock.get_fps - below is probably faster?
        # Also see lvgl macro define LV_USE_PERF_MONITOR
        fps_counter += 1
        if (timer_function() - start_time) >= 1:  # calc every 1 (one) second
            fps = fps_counter / (timer_function() - start_time)  # NOTE faster to call again than to store and use local variable
            #fps_str = "FPS: %f" % (fps,)
            fps_str = "FPS: %d" % (int(fps),)
            #print(fps_str)  # to serial
            display.draw_text8x8(fps_x, fps_y, fps_str, COLOR_WHITE, COLOR_BLACK)
            fps_counter = 0  # reset
            start_time = timer_function()

    paint_time()  # could be upto 2 secs before next paint?
    # try and figure out exactly when the next new whole-second starts

    wait_for_new_second_time = timer_function()
    while wait_for_new_second_time == timer_function():
        machine.idle()
    """
    # below should avoid any y38k issues....
    year, month, mday, hour, minute, second, weekday, yearday = local_time_tuple_function()
    new_second = second
    while new_second == second:  # busy loop...
        year, month, mday, hour, minute, new_second, weekday, yearday = local_time_tuple_function()
        machine.idle()
    """

    rtc = machine.RTC()
    #rtc.irq(trigger=rtc.ALARM0, handler=paint_time, wake=machine.IDLE)  # AttributeError: 'RTC' object has no attribute 'irq'
    # TODO doc reference to oddity with optional params that is specific to MicroPython
    rtc.irq(rtc.ALARM0, handler=paint_time, wake=machine.IDLE)  # AttributeError: 'RTC' object has no attribute 'irq'
    rtc.irq(rtc.ALARM0, handler=paint_time, wake=machine.SLEEP)
    rtc.irq(rtc.ALARM0, handler=paint_time, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, 1000, repeat=True)
    while True:
        machine.idle()
        #machine.deepsleep()
        #machine.lightsleep()

try:
    display_clock()
finally:
    cyd.cleanup()
