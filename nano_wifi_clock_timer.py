# nano_wifi_clock_timer.py

import machine
import network
import requests
import time

from color_setup import ssd  # Create a display instance
from gui.core.colors import RED, BLUE, GREEN, WHITE, BLACK
from gui.core.nanogui import refresh
from gui.core.writer import CWriter
import gui.fonts.arial35 as font
#import gui.fonts.freesans20 as font
from gui.widgets.label import Label

#from microwifimanager.manager import WifiManager

refresh(ssd, True)  # Initialise and clear display.

# Uncomment for ePaper displays
# ssd.wait_until_ready()


TIME_SERVER_URL = 'http://worldtimeapi.org/api/ip'

rtc = machine.RTC()
# NOTE expects local time set (via Thonny) for now

# setup functions for time, note this is both for API (readability) but it also massively impacts performance by reducing module lookup (almost 50fps with simple clock)
#timer_function = utime.time
timer_function = time.time

#local_time_tuple_function = utime.localtime
local_time_tuple_function = time.localtime  # NOTE **not** a struct under micropython!

COLOR_WHITE = WHITE
COLOR_BLACK = BLACK

fps_counter = 0
start_time = timer_function()
def display_clock():
    print('DEBUG start display_clock()')
    bg_color = COLOR_WHITE
    fg_color = COLOR_BLACK
    x, y = 0, 0
    #fps_x, fps_y = 100, 100
    #fps_x, fps_y = 0, 240 - 8
    fps_x, fps_y = 250, 240 - 8

    xpos = 0
    ypos = 0

    # Instantiate CWriter
    CWriter.set_textpos(ssd, 0, 0)  # In case previous tests have altered it
    wri = CWriter(ssd, font, bg_color, fg_color, verbose=False)
    wri.set_clip(True, True, False)

    label_time = Label(wri, 200, 2, 35)
    # nano fg and bg appear to be switched...
    #date_time = Label(wri, xpos, ypos, text=35, fgcolor=fg_color, bgcolor=bg_color)  # text is pixel width? (or string, '1234-12-12') seems to have no effect
    date_time = Label(wri, xpos, ypos, text='1234-12-12', fgcolor=fg_color, bgcolor=bg_color)  # text is pixel width? (or string, )

    print('DEBUG pre func def paint_time')
    def paint_time(timer_object):  # TODO should micropython.schedule() be used?
        print('DEBUG start paint_time()')
        global fps_counter
        global start_time

        l = local_time_tuple_function()
        time_str = '%02d:%02d:%02d' % (l[3], l[4], l[5])
        date_str = '%04d-%02d-%02d' % (l[0], l[1], l[2])
        label_time.value(time_str)
        date_time.value(date_str)
        """
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
        """
        refresh(ssd)
        print('DEBUG end paint_time()')

    one_second_timer = machine.Timer(0)  # NOTE esp32 only 4 timers

    paint_time(one_second_timer)  # could be upto 2 secs before next paint?
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

    # Now assume Timer is accurate enough now we have the second start time figured out
    #one_second_timer.init(period=1000, mode=machine.Timer.ONE_SHOT, callback=paint_time)
    one_second_timer.init(period=1000, mode=machine.Timer.PERIODIC, callback=paint_time)
    while True:
        machine.idle()
        # Can not use machine.lightsleep(), timer never wakes up (unless specify a sleep period). TODO RTC alarm...


def rtc_update():
    # NOTE this function will NOT set exact time, at best network fast and only lose time spent on code below
    try:
        response = requests.get(TIME_SERVER_URL)
        if response.status_code == 200:
            parsed = response.json()
            #iso_datetime_str = parsed['datetime']  # "2024-12-13T14:15:16.000000-12:30"
            #iso_datetime_str = iso_datetime_str[:-len("-12:30")]  # trim off timezone
            #iso_datetime_str = iso_datetime_str.replace('T', '-').replace(':', '-').replace('.', '-')
            year, month, day, hour, min, sec, microseconds = map(int, parsed['datetime'][:-len("-12:30")].replace('T', '-').replace(':', '-').replace('.', '-').split('-'))
            rtc.datetime((year, month, day, parsed["day_of_week"] - 1, hour, min, sec, microseconds))
            return True
    except:  # yep bare
        return False
    return False

try:
    print('DEBUG start of try')
    """
    ssid = 'SClock'
    network.hostname(ssid.lower())  # TODO + last 4 digits of mac?
    display.draw_text8x8(0, 10, 'Trying to start WiFi', COLOR_WHITE, COLOR_BLACK)
    display.draw_text8x8(0, 18, 'ssid: %s' % ssid, COLOR_WHITE, COLOR_BLACK)
    wlan = None
    while wlan is None:
        print("Trying to start WiFi network connection.")
        wlan = WifiManager(ssid=ssid).get_connection()
    print("Clock connected to WiFi network")
    print("%r" % (wlan.ifconfig(),))  # IP address, subnet mask, gateway, DNS server
    print("%r" % (wlan.config('mac'),))  # MAC in bytes
    print("SSID: %r" % (wlan.config('ssid'),))
    print("hostname: %r" % (network.hostname(),))

    display.draw_text8x8(0, 24, 'Connected %s Sync RTC' % wlan.config('ssid'), COLOR_WHITE, COLOR_BLACK)
    if rtc_update():
        display.clear()
    else:
        display.clear()
        display.draw_text8x8(0, 10, 'Failed to get and sync time', COLOR_BLACK, COLOR_WHITE)
    # now use wlan.ABC to check status, etc.
    """

    print('DEBUG pre; display_clock()')
    display_clock()
finally:
    # Leave screen alone/on for visual inspection - uncomment below to change that
    pass
