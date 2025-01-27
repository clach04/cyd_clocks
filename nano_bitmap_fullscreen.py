"""working for gray/grey scale 4-bit BUT not with 8-bit driver
working color 8-bit with 8-bit driver ONLY.

Not working for color with 4-bit driver, end up with garbage.

Suspect need to correct palette (or load lines in correct order due to display rotation?)

Grayscale/Greyscale

    py -3 img_cvt.py images/Philips_PM5544.pgm fullscreen.bin

Color 8-bit (not 16-bit)

    py -3 img_cvt.py images/Philips_PM5544.png fullscreen.bin

"""

from color_setup import ssd  # Create a display instance. NOTE edit to select 4-bit or 8-bit driver (there is no 16-bit driver)
from gui.core.nanogui import refresh


refresh(ssd)  # Initialise display.
fn = "fullscreen.bin"  # Image created by `img_cvt.py`
# The following line is required if a 4-bit driver is in use
#ssd.greyscale(True)  # NOTE if omitted, will get some colors - pallete undefined? NOTE2 - MISSING from 8-bit driver
with open(fn, "rb") as f:
    _ = f.read(4)  # Read and discard rows and cols ... or
    #rows = int.from_bytes(f.read(2), "big")
    #cols = int.from_bytes(f.read(2), "big")
    f.readinto(ssd.mvb)  # Read the image into the frame buffer
refresh(ssd)
