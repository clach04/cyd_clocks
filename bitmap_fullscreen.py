"""Landscape full screen load image
Create a file called fullscreen_320x240_rgb565.raw using img2rgb565.py
image needs to be 320x240 in raw rgb565 format.
"""
import cyd_wrap

def display_function():
    display = cyd.display
    display.clear()
    display.draw_image('fullscreen_320x240_rgb565.raw')  # created with https://github.com/rdagger/micropython-ili9341/blob/master/utils/img2rgb565.py

cyd = cyd_wrap.CYD()
try:
    display_function()
finally:
    # Leave screen alone/on for visual inspection - uncomment below to change that
    #cyd.cleanup()
    pass
