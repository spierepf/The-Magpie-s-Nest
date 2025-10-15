# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import network
import time
import secret

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Set the mDNS hostname
wlan.config(hostname=secret.MDNS_NAME)

# Connect to Wi-Fi
wlan.connect(secret.WIFI_CREDENTIALS['ssid'], secret.WIFI_CREDENTIALS['psk'])

while not wlan.isconnected():
    print('Waiting for connection...')
    time.sleep(1)

print('Connected to Wi-Fi!')
print('IP address:', wlan.ifconfig()[0])

print(f'mDNS hostname set to: {wlan.config("hostname")}.local')
