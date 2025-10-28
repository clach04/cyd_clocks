#! /usr/bin/env python3
"""Given a palletized image, should (already) be 320x240 4-bit (i.e. 16 colors)

Generate a raw image suitable for use with 4-bit driver in nano-GUI

TODO 8-bit support (skipping nibble code)
TODO move logic into https://github.com/clach04/image_convert
"""

import sys

from PIL import Image

import nano_4bit_pallette

is_py3 = sys.version_info >= (3,)

def mygetpalette(pal_type, orig_image_palette):
    # return palette list of tuples in RGB order
    palette = []
    if pal_type != "RGB":
        return palette
    image_palette = orig_image_palette[:]
    while image_palette != []:
        r = image_palette.pop(0)
        g = image_palette.pop(0)
        b = image_palette.pop(0)
        palette.append( (r, g, b) )
    return palette

argv = sys.argv

in_path = argv[1]
try:
    out_filename = argv[2]
except IndexError:
    out_filename = in_path + '.bin'

im = Image.open(in_path)

width, height = im.size
try:
    if im.info["transparency"] == 0:
        transparency = True
except KeyError:
    transparency = False

# FIXME more sanity checks
# FIXME sanity check; no transparency
# FIXME sanity check; bit depth 4 or less

# Sanity checks on assumptions
if 'getdata' not in dir(im.palette):
    raise NotImplementedError('image must be indexed, try a PNG or GIF')
pal_type, pal_data = im.palette.getdata()
if pal_type != "RGB":
    raise NotImplementedError('Need RGB palette, try a PNG file (instead of BMP)')

print(pal_data)
if is_py3:
    pal_data = list(pal_data)
else:
    pal_data = list(map(ord, pal_data))  # py2 bytes to ints

indexed_palette = mygetpalette(pal_type,pal_data) ## must contain accurate palette

print(indexed_palette)
for entry in indexed_palette:
    print(entry)
print('TODO review palette for accuracy')
# For now, just assume this is correct
assert indexed_palette == nano_4bit_pallette.nano_gui_palette_tuples

pixels = list(im.getdata())
"""
for x in im.getdata():
    print(x)
print('')
print(pixels)
"""

fo = open(out_filename, 'wb')

fo.write(b"".join((height.to_bytes(2, "big"), width.to_bytes(2, "big"))))

pixel_counter = 0
nibbles = [0, 0]
while pixel_counter < len(pixels):
    for n in range(2):
        c = pixels[pixel_counter]
        nibbles[n] = c
        pixel_counter += 1
    fo.write(int.to_bytes((nibbles[0] << 4) | nibbles[1], 1, "big"))

fo.close()
