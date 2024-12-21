# demo_pbm.py
# modified from https://github.com/rdagger/micropython-ili9341/blob/master/demo_pbm.py
# to work on my display
# NOTE needs invaders48x36.pbm from https://github.com/rdagger/micropython-ili9341/blob/master/images/invaders48x36.pbm
# 
"""ILI9341 demo (PBM - Portable Bitmap)."""
from framebuf import FrameBuffer, MONO_HLSB, RGB565  # type: ignore
import machine
from machine import Pin, SPI  # type: ignore
from struct import pack, unpack
from time import sleep

from ili9341 import Display, color565


def create_palette(foreground, background=0, invert=False):
    """Create framebuffer palette to translate between MONO_HLSB and RGB565.

    Args:
        foreground(int): Foreground color in RGB656 format
        background(int): Background color in RGB656 format (default Black)
        invert(bool): Invert foreground and background (default False)
    Returns:
        FrameBuffer: Color palette
    """
    # Need to swap endian colors
    foreground = unpack('>H', pack('<H', foreground))[0]
    background = unpack('>H', pack('<H', background))[0]

    # Buffer size equals 2 pixels (MONO_HLSB) x 2 byte color depth (RGB565)
    buffer_size = 4
    # Define framebuffer
    palette = FrameBuffer(bytearray(buffer_size), 2, 1, RGB565)
    # Set foreground & background color pixels (swap if inverted)
    palette.pixel(0 if invert else 1, 0, background)
    palette.pixel(1 if invert else 0, 0, foreground)
    return palette


def load_pbm(filename):
    """Load portable bitmap file.

    Args:
        filename(str): Path to bitmap
    Returns:
        tuple: A tuple containing the following:
            - FrameBuffer: The image data in MONO_HLSB format.
            - int: The width of the image.
            - int: The height of the image.
    """
    with open(filename, 'rb') as f:
        # Read and discard the first 2 lines
        for _ in range(2):
            f.readline()
        # Read dimensions from the third line
        dimensions = f.readline().split()
        width = int(dimensions[0])
        height = int(dimensions[1])

        # Read the bitmap data
        data = bytearray(f.read())
    return FrameBuffer(data, width, height, MONO_HLSB), width, height


def test():
    """Test code."""
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
    backlight.on()  # TODO review PWM instead of on/off
    display.clear()

    # Load invader .PBM image to framebuffer and get dimensions
    invader_fb, w, h = load_pbm('invaders48x36.pbm')

    # Create RGB565 placeholder
    placeholder = bytearray(w * h * 2)
    # Create frame buffer for placeholder
    placeholder_fb = FrameBuffer(placeholder, w, h, RGB565)
    # Draw invaders in different color palettes
    counter = 0
    for parameter in [
        (color565(255, 0, 0), 0, False, 0, 0),
        (color565(0, 255, 0), 0, False, 0, 54),
        (color565(0, 0, 255), 0, False, 0, 108),
        (color565(0, 255, 255), 0, False, 0, 162),
        (color565(255, 255, 0), 0, False, 0, 216),
        (color565(255, 0, 255), 0, False, 0, 270),
        (color565(255, 0, 0), 0, True, 64, 0),
        (color565(0, 255, 0), 0, True, 64, 54),
        (color565(0, 0, 255), 0, True, 64, 108),
        (color565(0, 255, 255), 0, True, 64, 162),
        (color565(255, 255, 0), 0, True, 64, 216),
        (color565(255, 0, 255), 0, True, 64, 270),
        (color565(255, 0, 0), color565(0, 255, 255), False, 128, 0),
        (color565(0, 255, 0), color565(255, 0, 255), False, 128, 54),
        (color565(0, 0, 255), color565(255, 255, 0), False, 128, 108),
        (color565(255, 255, 255), 0, False, 128, 162),
        (color565(255, 165, 0), 0, False, 128, 216),
        (color565(185, 0, 255), 0, False, 128, 270),
        (color565(255, 0, 0), color565(0, 255, 255), True, 191, 0),
        (color565(0, 255, 0), color565(255, 0, 255), True, 191, 54),
        (color565(0, 0, 255), color565(255, 255, 0), True, 191, 108),
        (color565(255, 255, 255), 0, True, 191, 162),
        (color565(255, 165, 0), 0, True, 191, 216),
        (color565(185, 0, 255), 0, True, 191, 270),
    ]:
        counter += 1
        print(counter, *parameter[3:5])
        x, y = parameter[3:5]
        palette = create_palette(*parameter[:3])
        placeholder_fb.blit(invader_fb, 0, 0, -1, palette)
        #display.draw_sprite(placeholder, *parameter[3:5], w, h)
        #display.draw_sprite(placeholder, x, y, w, h)
        display.draw_sprite(placeholder, y, x, w, h)

    sleep(10)

    leave_display_alone = True
    if not leave_display_alone:
        display.cleanup()
        backlight.off()


test()

