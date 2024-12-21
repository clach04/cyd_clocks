# modified from https://github.com/dmccreary/micropython-clocks-and-watches/blob/main/src/clock-digits-4.py
# TODO use framebuf and blit
"""12 hour clock demo using 7-segment style numbers.
With am/pm and seconds as (tiny) text.
"""
import machine
import utime
from utime import sleep, localtime

#from machine import Pin, SPI  # TODO style decision
from ili9341 import Display, color565


# Baud rate of 40000000 seems about the max
spi = machine.SPI(1, baudrate=40000000, sck=machine.Pin(14), mosi=machine.Pin(13))
# bgr-mode disabled for CYD2
display = Display(
            spi, dc=machine.Pin(2), cs=machine.Pin(15),
            rst=machine.Pin(15),
            width=320, height=240,  # ommit this and endup with square, with static on right hand side
            bgr=False,
            gamma=False
)

backlight = machine.Pin(21, machine.Pin.OUT)
backlight.on()  # TODO review

def oled_text( s, x, y, c=None):  # FIXME do not ignore last parameter
    # emulation of framebuf https://github.com/stlehmann/micropython-ssd1306/blob/master/ssd1306.py / http://docs.micropython.org/en/latest/library/framebuf.html
    display.draw_text8x8(x, y, s, color565(0, 0, 0), color565(255, 255, 255))  # FIXME use c parameter

def oled_line(x1, y1, x2, y2, c):  # FIXME do not ignore last parameter
    # emulation of FrameBuffer.line(x1, y1, x2, y2, c) http://docs.micropython.org/en/latest/library/framebuf.html
    #self.draw_line(x1, y1, x2, y2, c)  # FIXME use c parameter
    display.draw_line(x1, y1, x2, y2, color565(255, 255, 255))  # FIXME use c parameter

def oled_fill_rect(x, y, w, h, c):  # FIXME do not ignore last parameter
    # FIXME noop - can NOT locate docs for this in FrameBuffer. Assuming params
    #display.fill_rectangle(x, y, w, h, color)
    display.fill_rectangle(x, y, w, h, color565(255, 255, 255))


# (unexpected) monkeypatch!
display.text = oled_text
display.line = oled_line
display.fill_rect = oled_fill_rect


"""segment map A-G

https://en.wikipedia.org/wiki/Seven-segment_display

     -A-
    |   |
    F   B
    |   |
     -G-
    |   |
    E   C
    |   |
     -D-
"""
segmentMapping = [
  #a, b, c, d, e, f, g
  [1, 1, 1, 1, 1, 1, 0], # 0
  [0, 1, 1, 0, 0, 0, 0], # 1
  [1, 1, 0, 1, 1, 0, 1], # 2
  [1, 1, 1, 1, 0, 0, 1], # 3
  [0, 1, 1, 0, 0, 1, 1], # 4
  [1, 0, 1, 1, 0, 1, 1], # 5
  [1, 0, 1, 1, 1, 1, 1], # 6
  [1, 1, 1, 0, 0, 0, 0], # 7
  [1, 1, 1, 1, 1, 1, 1], # 8
  [1, 1, 1, 1, 0, 1, 1]  # 9
];

# TODO option for angle/rounded ends
def drawThickHorizLine(x1, x2, y, width):
    display.line(x1, y, x2, y, 1);
    if width > 1:
        display.line(x1, y+1, x2, y+1, 1);
    if width > 2:
        display.line(x1, y-1, x2, y-1, 1);
    if width > 3:
        display.line(x1, y+2, x2, y+2, 1);
    if width > 4:
        display.line(x1, y-2, x2, y-2, 1);

# TODO option for angle/rounded ends
def drawThickVertLine(y1, y2, x, width):
    display.line(x, y1, x, y2, 1);
    if width > 1:
        display.line(x+1, y1, x+1, y2, 1);
    if width > 2:
        display.line(x-1, y1, x-1, y2, 1);
    if width > 3:
        display.line(x+2, y1, x+2, y2, 1);
    if width > 4:
        display.line(x-2, y1, x-2, y2, 1);
        
# x and y are the center of the digit, size is the center to edge
def drawDigit(digit, x, y, size, width):  # FIXME does not clear existing digit on screen
  segmentOn = segmentMapping[digit];
  
  # Horizontal segments
  for i in [0, 3, 6]:
    if (segmentOn[i]):
      if (i==0): yOffset = 0 # top
      if (i==3): yOffset = size*2 # bottom element
      if (i==6): yOffset = size # middle
      # display.line(x - size, y+yOffset-size, x + size, y+yOffset-size, 1);
      drawThickHorizLine(x - size, x + size, y+yOffset-size, width)

  # Vertical segments
  for i in [1, 2, 4, 5]:
    if (segmentOn[i]) :
      if (i==1 or i==5):
          startY = y-size
          endY = y
      if (i==2 or i==4):
          startY = y
          endY = y + size
      if (i==4 or i==5): xOffset = -size
      if (i==1 or i==2): xOffset = +size
      xpos = x + xOffset
      # display.line(xpos, startY, xpos, endY, 1)
      drawThickVertLine(startY, endY, xpos, width)

def update_screen():
    #display.fill(0)  # TODO?
    # Scale factor of 4 is too large for 24-hour format display
    scale_factor = 3
    dr = 10 * scale_factor  # digit radius
    dch = 26 * scale_factor  # digit center height
    lm = 10  * scale_factor  # left margin for all 4-digits
    dw = (2 * dr) + 4  # digit width (2*dr + spacing between digits)
    cm = 8  * scale_factor # colon left margin
    width = 3 * scale_factor  # TODO review, can this be thicker? Needs offsets to be updated if changed
    
    # draw the hour digits
    hour = localtime()[3]
    # FIXME 24-hour option
    if hour > 12:
        hour = hour - 12
        am_pm = 'pm'
    else:
        am_pm = 'am'
    if hour < 10:
        # just draw the second digit
        drawDigit(hour, lm+dw, dch, dr, width)
    else:
        # TODO 24-hour support
        # FIXME with scale_factor != 1, this does not work well and looks ugly
        # we have 10, 11 or 12 so the first digit is 1
        drawDigit(1, lm, dch, dr, width)
        # subtract 10 from the second digit
        drawDigit(hour - 10, lm + dw, dch, dr, width)
       
    # draw the colon
    if localtime()[5] % 2:
        draw_colon(lm + dw * 2 + cm - (16 * scale_factor), dch - (5 * scale_factor), scale_factor)  # FIXME location needs work
    
    # draw the minutes
    minutes = localtime()[4]
    # value, x, y, size
    # left minute digit after the colon
    drawDigit(minutes // 10, lm + dw * 2 +cm, dch, dr, width)
    # right minute digit
    drawDigit(minutes % 10, lm + dw * 3 + cm + (2 * scale_factor), dch, dr, width)
    
    # draw the AM/PM
    display.text(am_pm, lm+dw*4+cm-8, dch+3, 1)  # TODO location (at-all? Use 24-hour)
    
    display.text('%02d' % localtime()[5], 0, 54)  # TODO location

    #display.show()  # TODO needed?

def draw_colon(x, y, scale_factor):
    display.fill_rect(x, y, (2 * scale_factor), (2 * scale_factor), 1)
    display.fill_rect(x, y + (8 * scale_factor), (2 * scale_factor), (2 * scale_factor), 1)

def timeStrFmt():
    hour = localtime()[3]
    if hour > 12:
        hour = hour - 12
        am_pm = ' pm'
    else: am_pm = ' am'
    # format minutes and seconds with leading zeros
    minutes = "{:02d}".format(localtime()[4])
    return str(hour) + ':' + minutes + am_pm


def display_clock():
    while True:
        update_screen()
        sleep(1)

try:
    display_clock()
finally:
    display.cleanup()
    spi.deinit()
    backlight.off()
