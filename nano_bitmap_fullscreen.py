"""working for gray/grey scale 4-bit BUT not with 8-bit driver
working color 8-bit with 8-bit driver ONLY.

Not working for color with 4-bit driver, end up with garbage. Suspect need to correct pixel format, img_cvt.py only seems to support 4-bit for non-color (or load lines in correct order due to display rotation?)

Memory note, error allocating buf/mvb:

    MemoryError: memory allocation failed, allocating 76800 bytes

on driver init for 8-bit can happen when something else has loaded first. For example main.py and/or boot.py

Grayscale/Greyscale

    py -3 img_cvt.py images/Philips_PM5544.pgm fullscreen.bin

Color 8-bit driver (not 16-bit)

    py -3 img_cvt.py -d None images/philips_pm5544.ppm fullscreen_8bit.bin
    py -3 img_cvt.py         images/philips_pm5544.ppm fullscreen_8bit.bin

    py -3 img_cvt.py -d None images/philips_pm5544.pgm fullscreen_4bit.bin
    py -3 img_cvt.py         images/philips_pm5544.pgm fullscreen_4bit.bin

For files already in the correct dimensions, no dithering gives better results.

"""

from color_setup import ssd  # Create a display instance. NOTE edit to select 4-bit or 8-bit driver (there is no 16-bit driver)
from gui.core.nanogui import refresh


refresh(ssd)  # Initialise display.
if hasattr(ssd, 'lut'):
    # for CYD - this is 4-bit, could be grayscale (14 colors) or color with a 16 color palette - self.mode == framebuf.GS4_HMSB
    fn = "fullscreen_4bit.bin"  # Image created by `img_cvt.py`
    # Either:
    # set palette manually or:
    #ssd.greyscale(True)
else:
    # for CYD - this is 8-bit - ssd.mode == framebuf.GS8
    fn = "fullscreen_8bit.bin"  # Image created by `img_cvt.py`

print('Using filename %s' % fn)
# The following line is required if a 4-bit driver is in use
#ssd.greyscale(True)  # NOTE if omitted, will get some colors - pallete undefined? NOTE2 - MISSING from 8-bit driver
with open(fn, "rb") as f:
    _ = f.read(4)  # Read and discard rows and cols ... or
    #rows = int.from_bytes(f.read(2), "big")
    #cols = int.from_bytes(f.read(2), "big")
    f.readinto(ssd.mvb)  # Read the image into the frame buffer
refresh(ssd)
