# color and screen size/direction/orientation test/demo
# Based on code from https://github.com/peterhinch/micropython-nano-gui?tab=readme-ov-file#23-verifying-hardware-configuration

from color_setup import ssd  # Create a display instance
from gui.core.colors import RED, BLUE, GREEN
from gui.core.nanogui import refresh

refresh(ssd, True)  # Initialise and clear display.

# Uncomment for ePaper displays
# ssd.wait_until_ready()

"""
(0,0)
 _
|_|  Red Square (outline or filled depending on filled variable below)
  \
   \ Green line
    \ _
     |_| Blue Square (outline/filled)
  (x, y)

For CYD - assumes USB port(s) on right hand-side
"""
filled = False  # useful to ensuring have perfect pixel end of screen
filled = True

ssd.fill(0)
ssd.line(0, 0, ssd.width - 1, ssd.height - 1, GREEN)  # Green diagonal corner-to-corner
ssd.rect(0, 0, 15, 15, RED, filled)  # Red square at top left
ssd.rect(ssd.width -15, ssd.height -15, 15, 15, BLUE, filled)  # Blue square at bottom right
refresh(ssd)
