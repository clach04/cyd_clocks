# used to quickly get online
"""Usefull for quick mip install

    import mip
    mip.install("github:peterhinch/micropython-nano-gui")  # this will pull down demos :-(
    #mip.install("github:peterhinch/micropython-nano-gui/drivers/ili93xx")
    # below do not work, which limit the usefulness of driver only install
    #mip.install("github:peterhinch/micropython-nano-gui/gui/core")
    #mip.install("github:peterhinch/micropython-nano-gui/gui/core/colors")
    #mip.install("github:peterhinch/micropython-nano-gui/gui/core/nanogui")
"""

import network

from microwifimanager.manager import WifiManager


ssid = 'cyd'
network.hostname(ssid.lower())  # TODO + last 4 digits of mac?


wlan = None
while wlan is None:
    print("Trying to start WiFi network connection.")
    wlan = WifiManager(ssid=ssid).get_connection()
print("Clock connected to WiFi network")
print("%r" % (wlan.ifconfig(),))  # IP address, subnet mask, gateway, DNS server
print("%r" % (wlan.config('mac'),))  # MAC in bytes
print("SSID: %r" % (wlan.config('ssid'),))
print("hostname: %r" % (network.hostname(),))
