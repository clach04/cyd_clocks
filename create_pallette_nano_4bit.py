#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab

import os
import sys


# import Pillow
try:
    # Pillow and PIL
    from PIL import Image, ImageDraw  # http://www.pythonware.com/products/pil/
except ImportError:
    import Image, ImageDraw  # Older namespace - http://www.pythonware.com/products/pil/


MONO_IMAGE = '1'  # https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes
COLOR_PALETTE_8BIT_IMAGE = 'P'  # https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes
image_format = 'png'
file_name = 'rainbow'

page_size = (320, 240)
width, height = page_size
im = Image.new(mode=COLOR_PALETTE_8BIT_IMAGE, size=page_size, color='white')


# from nano colors.py - https://github.com/peterhinch/micropython-nano-gui/blob/77f58af1fab27e0ec6ba959a2b04cd4061fa828f/gui/core/colors.py#L14..L27
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHTRED = (140, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (100, 100, 100)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
LIGHTGREEN = (0, 100, 0)
DARKGREEN = (0, 80, 0)
DARKBLUE = (0, 0, 90)
# 12, 13, 14 free for user definition
FILLER_12_GRAY = (75, 75, 75)
FILLER_13_GRAY = (150, 150, 150)
FILLER_14_GRAY = (200, 200, 200)
WHITE = (255, 255, 255)


color_list = ['RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE', 'PURPLE', 'WHITE']
color_list = [
    BLACK,
    GREEN,
    RED,
    LIGHTRED,
    BLUE,
    YELLOW,
    GREY,
    MAGENTA,
    CYAN,
    LIGHTGREEN,
    DARKGREEN,
    DARKBLUE,
    FILLER_12_GRAY,
    FILLER_13_GRAY,
    FILLER_14_GRAY,
    WHITE
]
print('color_list count = %d' % len(color_list))

# generate vertical bars
bar_width = int(width / len(color_list))
bar_height = height

offset = 0
for color in color_list:
    ImageDraw.Draw(im).rectangle([(offset, 0), (offset + bar_width, bar_height)], fill=color)
    offset += bar_width

im.save(file_name + '.' + image_format, image_format)
