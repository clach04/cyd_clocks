"""working for gray/grey scale 4-bit

Not working for color

end up with garbage.
Suspect need to correct palette (or load lines in correct order due to display rotation?)


    py -3 img_cvt.py images/Philips_PM5544.pgm fullscreen.bin

"""

from color_setup import ssd  # Create a display instance
from gui.core.nanogui import refresh


refresh(ssd)  # Initialise display.
fn = "fullscreen.bin"  # Image created by `img_cvt.py`
# The following line is required if a 4-bit driver is in use
ssd.greyscale(True)  # NOTE if omitted, will get some colors - pallete undefined?
with open(fn, "rb") as f:
    _ = f.read(4)  # Read and discard rows and cols
    f.readinto(ssd.mvb)  # Read the image into the frame buffer
refresh(ssd)
