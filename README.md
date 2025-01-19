# cyd_clocks

CYD clock experiments https://github.com/clach04/cyd_clocks

https://github.com/micropython/micropython code written for use with ESP32-2432S028R - an esp32 based device with built-in screen.

NOTE some scripts expect/need/rely on https://github.com/clach04/MicroWiFiManager/tree/mine

Hardware notes, printed ids:

ESP32-2432S028

on ESP32:
  * ESP-WROOM 32
  * FCC ID: 2AC7Z-ESP-WROOM32

LCD has printed TPM408-2.8

Relies on Micropython with library/libraries:

  * https://github.com/rdagger/micropython-ili9341/
  * https://github.com/peterhinch/micropython-nano-gui
  * https://github.com/de-dh/ESP32-Cheap-Yellow-Display-Micropython-LVGL/tree/main/demo_no_lvgl
      * Original https://github.com/rdagger/micropython-ili9341
  * https://github.com/witnessmenow/ESP32-Cheap-Yellow-Display/

The code in this repo was originally written to support MicroPython 1.19.1,
but may (soon) require MicroPython 1.24.1+.

NOTE on my device color reproduction is improved with changes in ILI9341 init,
either pass in `gamma=False` or modify driver with changes from https://github.com/de-dh/ESP32-Cheap-Yellow-Display-Micropython-LVGL/tree/main/demo_no_lvgl:

    self.write_cmd(self.GAMMASET, 0x02)
    sleep(.1)
    self.write_cmd(self.GAMMASET, 0x01)
    # TODO another; sleep(.1)


## Demos

## MicroPython Demos

  * color_setup.py - setup/config for using CYD with MicroPython Nano GUI https://github.com/peterhinch/micropython-nano-gui
  * hw_info.py - Dump device information out to the serial port
  * hw_info_cp.py - Limited CircuitPython version of hw_info.py - Dump device information out to the serial port and screen
  * wifi_clock_timer.py - WiFi clock. no touch screen or button control, configure network via SClock said, by opening http://192.168.4.1 (DNS captive portal doesn't work well). NOTE **http** not https.
  * cyd_demo.py - simple hardware demo. screen, RGB LED, light sensor, and touch screen
  * tiny_8x8_clock_always_paint.py - 8x8 font, not really readable - basic test including ISO date display
  * font_clock_always_paint.py - 12x24 font, still too small - basic test
  * font_clock_always_paint_UMB.py - 43x61 font (Ubuntu Mono Bold size 72, UbuntuMonoBold43x61numbers.c), currently too slow to be reliable for 1 second accuracy (needs accurate sleep math)
  * clock-digits-4.py - small 7-segment style digit, still too small but larger than above - basic test - NOTE Work In Progress, has painting issues
  * 01-rainbow-test.py - simple full screen rainbow color demo
  * demo_pbm.py - invader sprite/gfx blit demo - NOTE needs pbm https://github.com/rdagger/micropython-ili9341/blob/master/images/invaders48x36.pbm
  * cyd_wrap.py - simple wrapper
      * rainbow-test.py - simple full screen rainbow color demo
      * font_clock_timer_paint.py - simple font based clock

## CircuitPython Demos

In directory [circuitpython](./circuitpython).

  * bitmap_test.py - bitmap / picture / photo fullscreen demo
      * uses 240x320.bmp which is EBU_Colorbars converted into 24-bit Windows BitMap

## Test Images

Test cards from https://en.wikipedia.org/wiki/Test_card

  * SMPTE color bars: common NTSC test pattern https://en.wikipedia.org/wiki/File:SMPTE_Color_Bars.svg
  * Test card Philips PM5544: common PAL test pattern https://en.wikipedia.org/wiki/File:Philips_PM5544.svg
  * European Broadcasting Union color bar test patternfor Standard-definition television. EBU colour bars (4:3) https://en.wikipedia.org/wiki/File:EBU_Colorbars.svg

License either Public Domain or Creative Commons

See [images](./images).
