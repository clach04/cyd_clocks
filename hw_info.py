# hw_info.py
"""determine MicroPython (ESP32) hardware details
"""

import gc
import os
import platform
import sys

# MicroPython specific
import bluetooth
try:
    import esp
except ImportError:
    esp = None
import machine
import network


def printable_mac(in_bytes, seperator=':'):
    if seperator:
        return seperator.join(['%02x' % x for x in in_bytes])
    else:
        return in_bytes.hex()

print('gc.mem_free %r - pre-collect' % (gc.mem_free(),))
gc.collect()
print('gc.mem_free %r - post-collect' % (gc.mem_free(),))
print('os.uname %r' % (os.uname(),))
print('platform.platform %r' % (platform.platform(),))
print('sys.implementation %r' % (sys.implementation,))
print('sys.platform %r' % (sys.platform,))
print('sys.version %r' % (sys.version,))
print('sys.version_info %r' % (sys.version_info,))
print('machine.unique_id %r' % (machine.unique_id(),))
micropython_version = list(map(int, os.uname().release.split('.')))  # very complicated version of sys.implementation.version (which returns a tuple
print('micropython_version %r' % (micropython_version,))
if micropython_version > [1, 19, 1]:
    print('machine.unique_id %r' % (machine.unique_id().hex(),))
if esp:
    print('esp.flash_size() %r' % (esp.flash_size(),))
# TODO determine why esp.flash_id() is  ESP8266 only



wlan_ap = network.WLAN(network.AP_IF)
wlan_sta = network.WLAN(network.STA_IF)

# MAC is in bytes
cl_addr = printable_mac(wlan_sta.config('mac'))
ap_addr = printable_mac(wlan_ap.config('mac'))

print('Regular MAC      %r' % (wlan_sta.config('mac'),))
print('Regular MAC      %r' % (cl_addr,))
print('AP MAC           %r' % (ap_addr,))
try:
    print('network.hostname %r' % (network.hostname(),))
except AttributeError:
    # older micropython. 1.19? pre 1.24?
    print('network.hostname NOT_AVAILABLE_OLD_MP')
print('IP details %r' % (wlan_ap.ifconfig(),))

ble = bluetooth.BLE()  # defaults to addr_mode == PUBLIC 
ble.active(True)
ble_pub_addr = ble.config('mac')  # MAC tuple, with MAC in bytes
ble.active(False)

print('BT-LE Public MAC %r' % (ble_pub_addr,))
if micropython_version > [1, 19, 1]:
    print('BT-LE Public MAC %r' % (printable_mac(ble_pub_addr[1], seperator=''),))
print('BT-LE Public MAC %r' % (printable_mac(ble_pub_addr[1]),))

check_i2c_bus = False
if check_i2c_bus:
    # i2c
    # SoftI2C() returns nothing on CYD1
    # Not been able to init Hardware I2C() :-(
    SCL_pin_number = 22
    SDA_pin_number = 27

    #i2c = machine.I2C(1, machine.Pin(SCL_pin_number), machine.Pin(SDA_pin_number), freq=400000)  # create I2C peripheral at frequency of 400kHz
    #i2c = machine.SoftI2C(machine.Pin(SCL_pin_number), machine.Pin(SDA_pin_number), freq=400000)  # create I2C peripheral at frequency of 400kHz
    #i2c = machine.SoftI2C(machine.Pin(SDA_pin_number), machine.Pin(SCL_pin_number), freq=400000)  # create I2C peripheral at frequency of 400kHz
    #
    #i2c = machine.SoftI2C(SDA_pin_number, SCL_pin_number)  # NOTE I think this is reversed.... CYD1 and original CYD2 Returns [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119]
    i2c = machine.SoftI2C(machine.Pin(SDA_pin_number), machine.Pin(SCL_pin_number), freq=400000)  # NOTE I think this is reversed... NOTE micropython_version v1.19.1 needs Pins (not numbers), v1.24.1 does NOT
    for device_id in i2c.scan():
        print('found %02x (%d)' % (device_id, device_id))
