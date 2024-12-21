# 01-rainbow-test.py
"""From https://github.com/dmccreary/micropython-clocks-and-watches/blob/main/src/kits/ili9341/01-rainbow-test.py
Modified as did not work out of box for me
"""
# print out "Hello World!" using the rotation=3 using 32-bit high font
# the default is white text on a black background
from ili9341 import Display, color565
import machine
from machine import Pin, SPI

WIDTH = 320
HEIGHT = 240

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
            #gamma=True
            gamma=False  # improves color on my CYD2 device
)

backlight = machine.Pin(21, machine.Pin.OUT)
backlight_pwm = machine.PWM(backlight)
#backlight.on()  # TODO review PWM instead of on/off
#backlight_pwm.duty(1023)  # 100%
backlight_pwm.duty(512)  # 50%

RED = color565(255,0,0)
ORANGE = color565(255,128,0)
YELLOW = color565(255,255,0)
GREEN = color565(0,255,0)
BLUE = color565(0,0,255)
PURPLE = color565(255,0,255)
WHITE = color565(255,255,255)
BLACK = color565(0,0,0)

display.clear()

display.fill_rectangle(0,0, 50,HEIGHT, RED)
display.fill_rectangle(50,0, 50,HEIGHT, ORANGE)
display.fill_rectangle(100,0, 50,HEIGHT, YELLOW)
display.fill_rectangle(150,0, 50,HEIGHT, GREEN)
display.fill_rectangle(200,0, 50,HEIGHT, BLUE)
display.fill_rectangle(250,0, 50,HEIGHT, PURPLE)
display.fill_rectangle(300,0, 20,HEIGHT, WHITE)  # NOTE truncated/thin/narrow


print('Done')
