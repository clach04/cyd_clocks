# nano-GUI text hello world demo https://github.com/peterhinch/micropython-nano-gui
# NOTE additional documentation in https://github.com/peterhinch/micropython-font-to-py/blob/master/writer/WRITER.md
# calls refresh multiple times, as a quick sanity/speed check

from color_setup import ssd  # Create a display instance
from gui.core.colors import RED, BLUE, GREEN, WHITE, BLACK
from gui.core.nanogui import refresh
#import gui.fonts.arial10 as font
#import gui.fonts.arial35 as font
import gui.fonts.freesans20 as font
from gui.widgets.label import Label, ALIGN_LEFT, ALIGN_RIGHT, ALIGN_CENTER


from gui.core.writer import CWriter  # NOTE On a monochrome display Writer is more efficient than CWriter.

refresh(ssd, True)  # Initialise and clear display.

# Uncomment for ePaper displays, also see note about Writer versus CWriter
# ssd.wait_until_ready()


# https://docs.micropython.org/en/v1.15/library/framebuf.html#drawing-text
ssd.text('Hello World built-in', 0, 10, WHITE)  # 8x8 built in font, only have color control over text foreground
refresh(ssd)  # display to screen

bg_color = BLACK
fg_color = WHITE


# nano GUI
CWriter.set_textpos(ssd, 0, 0)  # In case previous code have altered it
wri = CWriter(ssd, font, fgcolor=fg_color, bgcolor=bg_color, verbose=False)
wri.set_clip(row_clip=True, col_clip=True, wrap=False)  # Clip to screen, no wrap

label_goodbye = Label(wri, 200, 2, 35)
label_goodbye.value('Goodbye World nano-GUI')
refresh(ssd)  # display to screen


# Bordered text demos

# 35 pixels set for length, which will be the width/length of the border - also used for alignment

#                     writer, row, col, text, invert=False, fgcolor=None, bgcolor=None, bdcolor=False, align=ALIGN_LEFT)
#label_bordered = Label(wri, 100, 2, 35, bdcolor=True)  # this doesn't work
label_bordered = Label(wri, 100, 2, 35, bdcolor=None)  # this is what the docs say but is confusing as it is still Falsey but has a different behavior
#label_bordered = Label(wri, 100, 2, 35, bdcolor=WHITE)  # this does work
label_bordered.value('bordered text from nano-GUI')
refresh(ssd)  # display to screen

#label_bordered_green = Label(wri, 150, 2, 35, bdcolor=GREEN)
label_bordered_green = Label(wri, 150, 2, 'green bordered text from nano-GUI', bdcolor=GREEN)
#label_bordered_green.value('green bordered text from nano-GUI')
refresh(ssd)  # display to screen


red_text_box_width = ssd.width - 4  # 2 pixels per side?
label_bordered_red = Label(wri, 70, 2, red_text_box_width, fgcolor=RED, bdcolor=RED, align=ALIGN_RIGHT)
label_bordered_red.value('red bordered text from nano-GUI')
refresh(ssd)  # display to screen
