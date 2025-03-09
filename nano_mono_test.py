# Mono / Black and White / 1-bit screen size/direction/orientation test/demo
# Based on nano_rgb_test.py

from color_setup import ssd  # Create a display instance
from gui.core.colors import BLACK, WHITE
from gui.core.nanogui import refresh

refresh(ssd, True)  # Initialise and clear display.

# Uncomment for ePaper displays  # TODO check bitdepth and make decisions, also Nano docs are inconcistent with code
# ssd.wait_until_ready()

"""
(0,0)
 _
|#|  Square filled
  \
   \  Line
    \ _
     |_|  Square outline
  (x, y) - max dimensions

For CYD - assumes USB port(s) on right hand-side
"""
fg = WHITE  # For now assume White  # TODO figure out what color to use for background and foreground
bg = BLACK  # default for now

ssd.fill(bg)
ssd.line(0, 0, ssd.width - 1, ssd.height - 1, fg)  # fg diagonal corner-to-corner  # TODO should this go corner to corner of screen or from inner-corner of squares?
ssd.rect(0, 0, 15, 15, fg, True)  # fg square filled at top left
ssd.rect(ssd.width -15, ssd.height -15, 15, 15, fg, False)  # fg square outline at bottom right
refresh(ssd)
