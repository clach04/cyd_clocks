# wifi_clock_timer.py
"""Micropython Clock that paints once a second, using Wifi Manager
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
import network
import ntptime
import requests
import time

#from machine import Pin, SPI  # TODO style decision
from ili9341 import Display, color565  # from https://github.com/rdagger/micropython-ili9341

from microwifimanager.manager import WifiManager

try:
    import posix_tz  # https://github.com/clach04/py-posix_tz
except ImportError:
    posix_tz = None

import cyd_wrap
from cyd_wrap import color565, WIDTH, HEIGHT

from umb43x61numbers import UMB  # load font. hopefully faster/cheaper than XglcdFont() load


def get_config(fn='clock.json'):  # TODO consider using https://github.com/Uthayamurthy/ConfigManager-Micropython (note it uses regexes...)
    # NOTE less memory if just try and open file and deal with errors
    try:
        with open(fn) as f:
            c = json.load(f)
    except:
        # yeah, bare except, gulp :-(
        c = {}
    # dumb update/merge for defaults
    c['TZ'] = c.get('TZ', 'PST8PDT,M3.2.0/2:00:00,M11.1.0/2:00:00')
    c['time_url'] = c.get('time_url', 'http://worldtimeapi.org/api/ip')
    # TODO NTP Server list
    return c

cyd = cyd_wrap.CYD()  # takes defaults, assumes CYD2 with 2 usb ports
display = cyd.display

config = get_config()

rtc = machine.RTC()
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

    def paint_time(timer_object):  # TODO should micropython.schedule() be used?
        global fps_counter
        global start_time

        l = local_time_tuple_function()
        time_str = '%02d:%02d:%02d' % (l[3], l[4], l[5])
        date_str = '%04d-%02d-%02d' % (l[0], l[1], l[2])
        display.draw_text(xpos, ypos + 100, time_str, umb, COLOR_WHITE)  # FIXME this does not clear existing written text, need to clear for clean output
        display.draw_text8x8(0, fps_y, date_str, COLOR_WHITE, COLOR_BLACK)

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

def rtc_update(config):
    if config['TZ']:
        print('Attempt NTP sync')
        ntptime.settime()  # TODO config for which server(s) to use for ntp time lookup.
        return True  # TODO check return result from above, for now assume alwasy successful... FIXME!

    print('Attempt http (REST) time sync')
    time_url = config['time_url']

    # NOTE this function will NOT set exact time, at best network fast and only lose time spent on code below
    print('Attempt to get time from online server %r' % time_url)
    try:
        response = requests.get(time_url)
        if response.status_code == 200:
            parsed = response.json()
            #iso_datetime_str = parsed['datetime']  # "2024-12-13T14:15:16.000000-12:30"
            #iso_datetime_str = iso_datetime_str[:-len("-12:30")]  # trim off timezone
            #iso_datetime_str = iso_datetime_str.replace('T', '-').replace(':', '-').replace('.', '-')
            year, month, day, hour, min, sec, microseconds = map(int, parsed['datetime'][:-len("-12:30")].replace('T', '-').replace(':', '-').replace('.', '-').split('-'))
            rtc.datetime((year, month, day, parsed["day_of_week"] - 1, hour, min, sec, microseconds))
            print('Set RTC')
            return True
        print('response.status_code %r' % response.status_code)
        print('response %r' % response)
        print('response.content %r' % response.content)
    except Exception as ex_info:  # yep bare
        print(ex_info)
        return False
    return False

try:
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

    print('pause for wifi to really be up')
    time.sleep(1)  # 1 second

    if rtc_update(config):
        display.clear()
    else:
        display.clear()
        display.draw_text8x8(0, 10, 'Failed to get and sync time', COLOR_BLACK, COLOR_WHITE)

    if posix_tz:
        posix_tz.set_tz(config['TZ'])
        print('time: %r' % (local_time_tuple_function(),))
        local_time_tuple_function = posix_tz.localtime
        print('TZ adjusted time: %r' % (posix_tz.localtime(),))

    # now use wlan.ABC to check status, etc.

    display_clock()
finally:
    cyd.cleanup()
