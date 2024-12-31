# hw_info.py
"""determine MicroPython (ESP32) hardware details
"""

import bluetooth
try:
    import esp
except ImportError:
    esp = None
import machine
import network
import os
import platform
import sys


print('os.uname %r' % (os.uname(),))
print('platform.platform %r' % (platform.platform(),))
print('sys.implementation %r' % (sys.implementation,))
print('sys.platform %r' % (sys.platform,))
print('sys.version %r' % (sys.version,))
print('sys.version_info %r' % (sys.version_info,))
print('machine.unique_id %r' % (machine.unique_id(),))
print('machine.unique_id %r' % (machine.unique_id().hex(),))
if esp:
    print('esp.flash_size() %r' % (esp.flash_size(),))
# TODO determine why esp.flash_id() is  ESP8266 only



wlan_ap = network.WLAN(network.AP_IF)
wlan_sta = network.WLAN(network.STA_IF)

ap_addr = wlan_ap.config('mac').hex()  # MAC in bytes
cl_addr = wlan_sta.config('mac').hex()  # MAC in bytes

print('AP MAC           %r' % (ap_addr,))
print('Regular MAC      %r' % (cl_addr,))

ble = bluetooth.BLE()  # defaults to addr_mode == PUBLIC 
ble.active(True)
ble_pub_addr = ble.config('mac')  # MAC tuple, with MAC in bytes
ble.active(False)

print('BT-LE Public MAC %r' % (ble_pub_addr,))
print('BT-LE Public MAC %r' % (ble_pub_addr[1].hex(),))

