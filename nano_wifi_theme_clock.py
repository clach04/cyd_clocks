# nano_wifi_theme_clock.py
"""This is not as reliable as the (non=theme) raw driver version.

Often get network issues, failure to sync RTC.
Sometimes get MicroPython crashes when connecting to WiFi with a panic and crashdump
Using 4-bit driver helps reduce chance, as does garbage collection
"""

import gc
import json
import machine
import network
import os
import requests
import time

from color_setup import ssd  # Create a display instance
from gui.core.colors import create_color, RED, BLUE, GREEN, WHITE, BLACK
from gui.core.nanogui import refresh
from gui.core.writer import CWriter
import gui.fonts.arial35 as font
#import gui.fonts.freesans20 as font
from gui.widgets.label import Label, ALIGN_LEFT, ALIGN_RIGHT, ALIGN_CENTER

print('gc.mem_free %r - pre-collect' % (gc.mem_free(),))
gc.collect()
print('gc.mem_free %r - post-collect' % (gc.mem_free(),))
try:
    raise ImportError  # DEBUG to save time
    # NOTE this may fail due to lack of memory
    from microwifimanager.manager import WifiManager
#except:
except ImportError:
    WifiManager = None

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

str2alignment = {
    "LEFT": ALIGN_LEFT,
    "CENTER": ALIGN_CENTER,
    "RIGHT": ALIGN_RIGHT
}

def str2rgb(in_str):
    r, g, b = map(int, in_str.split(','))  # assume int works with spaces
    return r, g, b

fps_counter = 0
start_time = timer_function()
one_second_timer = machine.Timer(0)  # NOTE esp32 only 4 timers
def display_clock(theme_config):
    #print('DEBUG display_clock() start')
    theme_config["DATE"] = theme_config.get("DATE", {})
    theme_config["TIME"] = theme_config.get("TIME", {})

    # TODO background image - "BACKGROUND"
    # TODO background color(s) - "BACKGROUND_COLOR"
    # TODO palette (from background image - "BACKGROUND" ? or new config entries)
    # TODO background color(s) - "INTERVAL"
    date_format = theme_config["DATE"].get("FORMAT", "YYYY-MM-dd")
    time_format = theme_config["TIME"].get("FORMAT", "HH:mm:ss")

    default_color_str = theme_config.get("FONT_COLOR", "255, 255, 255")
    r, g, b = str2rgb(default_color_str)

    # # 12, 13, 14 free for user definition
    fg_color = create_color(12, r, g, b)  # FIXME hard coded literal, replace with micropython constant

    color_str = theme_config["TIME"].get("FONT_COLOR", default_color_str)
    if default_color_str == color_str:
        time_color = fg_color
    else:
        r, g, b = str2rgb(color_str)
        time_color = create_color(13, r, g, b)  # FIXME hard coded literal, replace with micropython constant

    color_str = theme_config["DATE"].get("FONT_COLOR", default_color_str)
    if default_color_str == color_str:
        date_color = fg_color
    else:
        r, g, b = str2rgb(color_str)
        date_color = create_color(14, r, g, b)  # FIXME hard coded literal, replace with micropython constant

    bg_color = WHITE

    fps_x, fps_y = 250, 240 - 8

    # Instantiate CWriter
    CWriter.set_textpos(ssd, 0, 0)  # In case previous tests have altered it
    wri = CWriter(ssd, font, bg_color, fg_color, verbose=False)
    wri.set_clip(True, True, False)

    # FIXME  bgcolor=BLACK hard coded
    label_time = Label(wri, theme_config["TIME"].get("Y", 0), theme_config["TIME"].get("X", 0), text=theme_config["TIME"].get("WIDTH", time_format), fgcolor=time_color, bgcolor=BLACK, align=str2alignment.get(theme_config["TIME"].get("ALIGNMENT", "LEFT"), ALIGN_LEFT))  # FIXME map time_format to text with only zeros
    date_time  = Label(wri, theme_config["DATE"].get("Y", 0), theme_config["DATE"].get("X", 0), text=theme_config["DATE"].get("WIDTH", date_format), fgcolor=date_color, bgcolor=BLACK, align=str2alignment.get(theme_config["DATE"].get("ALIGNMENT", "LEFT"), ALIGN_LEFT))  # FIXME map date_format to text with only zeros
    # FIXME bgcolor, potentially border support too

    def paint_time(timer_object):  # TODO should micropython.schedule() be used?
        #print('DEBUG paint_time() start')
        global fps_counter
        global start_time

        l = local_time_tuple_function()
        # TODO don't update date if not changed
        time_str = '%02d:%02d:%02d' % (l[3], l[4], l[5])  # FIXME map time_format, currently hard coded
        date_str = '%04d-%02d-%02d' % (l[0], l[1], l[2])  # FIXME map date_format, currently hard coded
        label_time.value(time_str)
        date_time.value(date_str)

        """
        # About 4-5 FPS with date and time in arial35
        # simple FPS math. Consider implementing a clone of pygame.time.Clock() which has a tick()/get_fps() interface https://www.pygame.org/docs/ref/time.html#pygame.time.Clock.get_fps - below is probably faster?
        # Also see lvgl macro define LV_USE_PERF_MONITOR
        fps_counter += 1
        if (timer_function() - start_time) >= 1:  # calc every 1 (one) second
            fps = fps_counter / (timer_function() - start_time)  # NOTE faster to call again than to store and use local variable
            #fps_str = "FPS: %f" % (fps,)
            fps_str = "FPS: %d" % (int(fps),)
            print(fps_str)  # to serial
            print((fps_x, fps_y, fps_str, WHITE))  # to serial
            # need to blank out fps text otherwise will overpaint
            ssd.rect(fps_x, fps_y, 8 * 8, 15, BLUE, True)
            ssd.text(fps_str, fps_x, fps_y, WHITE)  # 8x8 built in font  - unsure how to pass in 8x8 font into Label widget
            #ssd.text(250, 240 - 8, 'hello')  # 8x8 built in font  - unsure how to pass in 8x8 font into Label widget
            #ssd.text(0, 10, 'Trying to start WiFi', WHITE)  # 8x8 built in font
            #WRONG PARAM ORDER ssd.text(0, 10, 'Hellow')  # 8x8 built in font - fails here (works on init) with; TypeError: can't convert 'int' object to str implicitly
            fps_counter = 0  # reset
            start_time = timer_function()
        """

        refresh(ssd)


    '''
    while True:
        paint_time(None)  # run in a loop to measure FPS
    '''


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
        print('response.status_code %r' % response.status_code)
        print('response %r' % response)
        print('response.content %r' % response.content)
    except Exception as ex_info:  # yep bare
        print(ex_info)
        return False
    return False

try:
    if not WifiManager:
        ssd.text('no WifiManager!', 0, 18*5, WHITE)
    else:
        ssid = 'SClock'
        network.hostname(ssid.lower())  # TODO + last 4 digits of mac?
        ssd.text('Trying to start WiFi', 0, 10, WHITE)  # 8x8 built in font
        ssd.text('ssid: %s' % ssid, 0, 18, WHITE)
        refresh(ssd)
        wlan = None
        wfm = WifiManager(ssid=ssid)
        while wlan is None:
            print("Trying to start WiFi network connection.")
            wlan = wfm.get_connection()
        print("Clock connected to WiFi network")
        print("%r" % (wlan.ifconfig(),))  # IP address, subnet mask, gateway, DNS server
        print("%r" % (wlan.config('mac'),))  # MAC in bytes
        print("SSID: %r" % (wlan.config('ssid'),))
        print("hostname: %r" % (network.hostname(),))
        del(wfm)

        ssd.text('Connected %s Sync RTC' % wlan.config('ssid'), 0, 24, WHITE)
        refresh(ssd)
        if rtc_update():
            refresh(ssd, True)  # Initialise and clear display.
        else:
            refresh(ssd, True)  # Initialise and clear display.
            ssd.text('Failed to get and sync time', 0, 10, WHITE)
        # now use wlan.ABC to check status, etc.

    """
    ssd.text('MicroPython!', 0, 0, WHITE)
    ssd.text('MicroPython!', 0, 18, WHITE)
    ssd.text('MicroPython!', 0, 18*2, WHITE)
    ssd.text('MicroPython!', 0, 18*3, WHITE)
    ssd.text('MicroPython!', 0, 18*4, WHITE)
    """
    refresh(ssd)

    """
    if hasattr(ssd, 'lut'):
        # for CYD - this is 4-bit, could be grayscale (14 colors) or color with a 16 color palette - self.mode == framebuf.GS4_HMSB
        fn = "fullscreen_4bit.bin"
        # Either:
        # set palette manually or:
        #ssd.greyscale(True)
    else:
        # for CYD - this is 8-bit - ssd.mode == framebuf.GS8
        fn = "fullscreen_8bit.bin"
    print('Using filename %s' % fn)
    # The following line is required if a 4-bit driver is in use
    #ssd.greyscale(True)  # NOTE if omitted, will get some colors - pallete undefined? NOTE2 - MISSING from 8-bit driver
    with open(fn, "rb") as f:
        _ = f.read(4)  # Read and discard rows and cols ... or
        #rows = int.from_bytes(f.read(2), "big")
        #cols = int.from_bytes(f.read(2), "big")
        f.readinto(ssd.mvb)  # Read the image into the frame buffer
    #refresh(ssd)
    """

    # NOTE less memory if just try and open file and deal with errors
    def file_or_dir_exists(filename):
        try:
            os.stat(filename)
            return True
        except OSError:
            return False

    theme_filename = "theme.json"
    #if not os.path.exists(theme_filename):
    if not file_or_dir_exists(theme_filename):
        theme = {}
    else:
        print('DEBUG open file')
        f = open(theme_filename)
        print('DEBUG load file')
        theme = json.load(f)  # NOTE this is not quick
        print('DEBUG close file')
        f.close()
    #display_clock({})  # DEBUG TODO load json file from disk
    display_clock(theme)
finally:
    # Leave screen alone/on for visual inspection - uncomment below to change that
    pass
    one_second_timer.deinit()  # stop updating the clock/time
