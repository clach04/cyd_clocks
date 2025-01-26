# from https://github.com/peterhinch/micropython-nano-gui?tab=readme-ov-file#23-verifying-hardware-configuration

from color_setup import ssd  # Create a display instance
from gui.core.colors import RED, BLUE, GREEN
from gui.core.nanogui import refresh

refresh(ssd, True)  # Initialise and clear display.

# Uncomment for ePaper displays
# ssd.wait_until_ready()

"""
 _
|_|  Red Square (outline)
  \
   \ Green line
    \ _
     |_| Blue Square (outline)

"""
ssd.fill(0)
ssd.line(0, 0, ssd.width - 1, ssd.height - 1, GREEN)  # Green diagonal corner-to-corner
ssd.rect(0, 0, 15, 15, RED)  # Red square at top left
ssd.rect(ssd.width -15, ssd.height -15, 15, 15, BLUE)  # Blue square at bottom right
refresh(ssd)
