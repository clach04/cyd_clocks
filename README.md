# cyd_clocks

CYD clock experiments https://github.com/clach04/cyd_clocks

Written for use with ESP32-2432S028R - an esp32 based device with built-in
screen. Relies on Micropython with library/libraries:

  * https://github.com/de-dh/ESP32-Cheap-Yellow-Display-Micropython-LVGL/tree/main/demo_no_lvgl
      * Original https://github.com/rdagger/micropython-ili9341
  * https://github.com/witnessmenow/ESP32-Cheap-Yellow-Display/

Demos:

  * tiny_8x8_clock_always_paint.py - 8x8 font, not really readable - basic test including ISO date display
  * tiny_8x8_clock_always_paint_framebuf.py - NOT working https://github.com/clach04/cyd_clocks/issues/2
  * font_clock_always_paint.py - 12x24 font, still too small - basic test
  * clock-digits-4.py - small 7-segment style digit, still too small but larger than above - basic test - NOTE Work In Progress, has painting issues
