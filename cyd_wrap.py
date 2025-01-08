# cyd_wrap.py
"""Simple wrapper for display of CYD
For now handles:

  Display and brightness

TODO RGB LED
    With pulse https://docs.micropython.org/en/latest/esp8266/tutorial/pwm.html#fading-an-led

NOTE experiments with v1 CYD...
"""

import machine

from ili9341 import Display, color565  # from https://github.com/rdagger/micropython-ili9341

# Consider putting these into a config module?
PIN_sck = 14
PIN_mosi = 13
PIN_dc = 2
PIN_cs = 15
PIN_rst = 15

WIDTH = 320
HEIGHT = 240

# TODO consider using const?
# EDIT_ME!
number_of_usb_ports = 1
number_of_usb_ports = 2

if number_of_usb_ports == 1:
    default_bgr = True
    default_gamma = True
    default_rotation = 270
else:  # if number_of_usb_ports == 2:
    default_bgr = False
    default_gamma = False
    default_rotation = 0

# TODO mirror support?

class CYD():
    def __init__(self,
        sck=PIN_sck, mosi=PIN_mosi,  # SPI
        dc=PIN_dc, cs=PIN_cs, rst=PIN_rst,  # ili9341 display
        width=WIDTH, height=HEIGHT,
        backlight_percentage=50,
        bgr=default_bgr,  # False for CYD2 with 2 USB ports (includes USB-C) - rgb/bgr switch
        gamma=default_gamma,  # False improves color on my CYD2 device (orange looks Brown by default). On CYD1 minor difference, True is slightly better for Orange
        rotation=default_rotation,  # CYD1 270 matches CYD2 0. With CYD1 (0,0) top-left appears to be portrait with USB port top-right. With CYD2 (0,0) top-left landscape with USB port bottom-right
        self_cleanup = True
    ):
        self.self_cleanup = self_cleanup

        # Baud rate of 40000000 seems about the max
        self.spi = machine.SPI(1, baudrate=40000000, sck=machine.Pin(sck), mosi=machine.Pin(mosi))
        # display = Display(spi, dc=Pin(4), cs=Pin(16), rst=Pin(17))
        # TODO see if can use lvgl API, which has different parameters
        # bgr-mode disabled for CYD2
        self.display = Display(
                    self.spi,
                    dc=machine.Pin(dc), cs=machine.Pin(cs), rst=machine.Pin(rst),
                    width=width, height=height,  # omit this and endup with square, with static on right hand side
                    rotation=rotation,
                    bgr=bgr,
                    gamma=gamma
        )

        self.backlight = machine.Pin(21, machine.Pin.OUT)
        self.backlight_pwm = machine.PWM(self.backlight)
        #backlight.on()  # PWM preffered instead of on/off
        #backlight_pwm.duty(1023)  # 100%
        #backlight_pwm.duty(512)  # 50%
        # TODO ensure backlight_percentage is 0-100
        self.backlight_pwm.duty(int(backlight_percentage * 10.23))  # 1023 / 100

    def cleanup(self):
        # TODO protect against multuple calls?
        self.display.cleanup()  # NOTE generates serial output, "display off"
        self.spi.deinit()
        self.backlight_pwm.duty(0)  # probably overkill
        self.backlight_pwm.deinit()
        self.backlight.off()

    def __del__(self):
        # NOTE this never seems to get called
        print('CYD delete requested')  # to serial port
        if self.self_cleanup:
            print('CYD attempt cleanup')  # to serial port
            self.cleanup()
