# based on https://github.com/witnessmenow/ESP32-Cheap-Yellow-Display/blob/main/Examples/Micropython/demo.py

from machine import Pin, SPI, SoftSPI, SDCard, ADC, idle
import os

# https://github.com/rdagger/micropython-ili9341
from ili9341 import Display, color565
from xpt2046 import Touch

import cyd_wrap
from cyd_wrap import color565, WIDTH, HEIGHT


cyd = cyd_wrap.CYD()  # takes defaults, assumes CYD2 with 2 usb ports
display = cyd.display

display_spi = display.spi

# Clear display to yellow
display.clear(color565(255, 255, 0))

# TODO move into cyd_wrap (potentially fake as a NeoPixel?)
# RGB LED at the back
red_led = Pin(4, Pin.OUT)
green_led = Pin(16, Pin.OUT)
blue_led = Pin(17, Pin.OUT)

# Turn on all LEDs (active low)
# RGB LED (and backlight) will also work with machine.PWM for dimming

red_led.off()
green_led.off()
blue_led.off()

if False:  # skip SD card test/demo
    # Set up SD card 
    sd = SDCard(slot=2, sck=Pin(18), miso=Pin(19), mosi=Pin(23), cs=Pin(5))
    # Print SD card info (seems to be card size and sector size?)
    print(sd.info())

    # Mount SD card and print directory listing
    # SD card must be formatted with a file system recognised by ESP32 (FAT)
    os.mount(sd, "/sd")
    print(os.listdir("/sd"))


# TODO move into cyd_wrap
# Read light sensor
lightsensor = ADC(34, atten=ADC.ATTN_0DB)
print(lightsensor.read_uv())  # my CYD1 always returns 75000 (from reports online, often this does not work)


# TODO move into cyd_wrap - also use SoftSPI to avoid conflicts.
# Read touch screen
#touch_spi = SPI(1, baudrate=1_000_000, sck=Pin(25), mosi=Pin(32), miso=Pin(39))
#touch_spi = SoftSPI(baudrate=1_000_000, sck=Pin(25), mosi=Pin(32), miso=Pin(39))
touch_spi = SoftSPI(sck=Pin(25), mosi=Pin(32), miso=Pin(39))  # unclear on baud rate, may be 2.5Mhz?

def touchscreen_press(x, y):
    print("Touch at " + str(x) + "," + str(y))  # only seems to work for single-press-and-release, not continuous drawing (possibly due to debounce code?)

touch = Touch(touch_spi, cs=Pin(33), int_pin=Pin(36), int_handler=touchscreen_press)
#touch = Touch(touch_spi, cs=Pin(33), int_handler=touchscreen_press)  # this does NOT work

# loop to wait for touchscreen test
try:
    while True:
        touch.get_touch()

except KeyboardInterrupt:
    print("\nCtrl-C pressed.  Cleaning up and exiting...")
finally:
    display.cleanup()
