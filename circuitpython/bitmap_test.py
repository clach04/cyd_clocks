# from https://github.com/adafruit/circuitpython/issues/9151
# extracted/fixed up from https://github.com/adafruit/circuitpython/issues/9151#issuecomment-2041203256

# I used CircuitPython with ttgo display and it worked as expected out of the box . In the case of sunton_esp32_2432S028 i used the default with the bin from here https://circuitpython.org/board/sunton_esp32_2432S028/ The text does not work as in the pic , the code i used for Bitmap is copy paste from the site

import board
import displayio
import time
import pulseio

board.DISPLAY.brightness = 0
splash = displayio.Group()
board.DISPLAY.root_group = splash

#filename = '/LVGL_320_240.bmp'
filename = '/240x320.bmp'
odb = displayio.OnDiskBitmap(filename)
face = displayio.TileGrid(odb, pixel_shader=odb.pixel_shader)
splash.append(face)

# Wait for the image to load.
board.DISPLAY.refresh(target_frames_per_second=60)

# Fade up the backlight
for i in range(100):
    board.DISPLAY.brightness = 0.01 * i
    time.sleep(0.05)

# Wait forever
while True: pass

# On exit/completion display will reset and image will be lost from screen
