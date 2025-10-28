# PIL / Pillow suitable palette definition
# https://github.com/clach04/cyd_clocks/issues/40#issuecomment-2676022881
# Also see https://github.com/clach04/image_convert/tree/main/palettes

# https://github.com/peterhinch/micropython-nano-gui/blob/77f58af1fab27e0ec6ba959a2b04cd4061fa828f/gui/core/colors.py#L14..L27
nano_gui_palette = [
    0, 0, 0,        # BLACK
    0, 255, 0,      # GREEN
    255, 0, 0,      # RED
    140, 0, 0,      # LIGHTRED  (actually dark-red)
    0, 0, 255,      # BLUE
    255, 255, 0,    # YELLOW
    100, 100, 100,  # GREY
    255, 0, 255,    # MAGENTA
    0, 255, 255,    # CYAN
    0, 100, 0,      # LIGHTGREEN
    0, 80, 0,       # DARKGREEN
    0, 0, 90,       # DARKBLUE
    75, 75, 75,     # 12 light-Grey  # NOTE not a reserved nano-color
    150, 150, 150,  # 13 darker-Grey  # NOTE not a reserved nano-color
    200, 200, 200,  # 14 darkest-Grey  # NOTE not a reserved nano-color
    255, 255, 255,  # WHITE
]
NANO_COLOR_BLACK = 0
NANO_COLOR_GREEN = 1
NANO_COLOR_RED = 2
NANO_COLOR_LIGHTRED = DARKRED = 3  # mislabeled - https://github.com/peterhinch/micropython-nano-gui/issues/95
NANO_COLOR_BLUE = 4
NANO_COLOR_YELLOW = 5
NANO_COLOR_GREY = 6
NANO_COLOR_MAGENTA = 7
NANO_COLOR_CYAN = 8
NANO_COLOR_LIGHTGREEN = 9
NANO_COLOR_DARKGREEN = 10
NANO_COLOR_DARKBLUE = 11
NANO_COLOR_LIGHTGREY = 12  # NOTE not a reserved nano-color
NANO_COLOR_DARKERGREY = 13  # NOTE not a reserved nano-color
NANO_COLOR_DARKESTGREY = 14  # NOTE not a reserved nano-color
NANO_COLOR_WHITE = 15

# ...

mode = 'P'  # palette
screen_res = (320, 240)
image = Image.new(mode, screen_res, background_color)
image.putpalette(nano_gui_palette)  # setup palette/index
draw = ImageDraw.Draw(image)
