# cyd_clocks

CYD clock experiments https://github.com/clach04/cyd_clocks

Written for use with ESP32-2432S028R - an esp32 based device with built-in
screen.

Hardware notes, printed ids:

ESP32-2432S028

on ESP32:
  * ESP-WROOM 32
  * FCC ID: 2AC7Z-ESP-WROOM32

LCD has printed TPM408-2.8

Relies on Micropython with library/libraries:

  * https://github.com/de-dh/ESP32-Cheap-Yellow-Display-Micropython-LVGL/tree/main/demo_no_lvgl
      * Original https://github.com/rdagger/micropython-ili9341
  * https://github.com/witnessmenow/ESP32-Cheap-Yellow-Display/

NOTE on my device color reproduction is improved with changes in ILI9341 init,
either pass in `gamma=False` or modify driver with changes from https://github.com/de-dh/ESP32-Cheap-Yellow-Display-Micropython-LVGL/tree/main/demo_no_lvgl:

    self.write_cmd(self.GAMMASET, 0x02)
    sleep(.1)
    self.write_cmd(self.GAMMASET, 0x01)
    # TODO another; sleep(.1)


Demos:

  * hw_info.py - Dump device information out to the serial port
  * wifi_clock_timer.py - WiFi clock. no touch screen or button control, configure network via SClock said, by opening http://192.168.4.1 (DNS captive portal doesn't work well). NOTE **http** not https.
  * tiny_8x8_clock_always_paint.py - 8x8 font, not really readable - basic test including ISO date display
  * font_clock_always_paint.py - 12x24 font, still too small - basic test
  * font_clock_always_paint_UMB.py - 43x61 font (Ubuntu Mono Bold size 72, UbuntuMonoBold43x61numbers.c), currently too slow to be reliable for 1 second accuracy (needs accurate sleep math)
  * clock-digits-4.py - small 7-segment style digit, still too small but larger than above - basic test - NOTE Work In Progress, has painting issues
  * 01-rainbow-test.py - simple full screen rainbow color demo
  * demo_pbm.py - invader sprite/gfx blit demo - NOTE needs pbm https://github.com/rdagger/micropython-ili9341/blob/master/images/invaders48x36.pbm
  * cyd_wrap.py - simple wrapper
      * rainbow-test.py - simple full screen rainbow color demo
      * font_clock_timer_paint.py - simple font based clock
