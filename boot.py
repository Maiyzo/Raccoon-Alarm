# Establish Internet connection
from network import WLAN, STA_IF
from network import mDNS
import time

wlan = WLAN(STA_IF)
wlan.active(True)

#wlan.connect('ME100-2.4G', '122Hesse', 5000)
wlan.connect('Hearst-Properties', '23Hearst$1&7', 5000)

tries = 0
while not wlan.isconnected() and tries < 10:
    print("Waiting for wlan connection")
    time.sleep(1)
    tries = tries + 1

if wlan.isconnected():
        print("WiFi connected at", wlan.ifconfig()[0])
else:
        print("Unable to connect to WiFi")

# Advertise as 'hostname', alternative to IP address
try:
    hostname = "Matt_ESP32"
    mdns = mDNS(wlan)
    # mdns.start(hostname, "MicroPython REPL")
    # mdns.addService('_repl', '_tcp', 23, hostname)
    mdns.start(hostname,"MicroPython with mDNS")
    _ = mdns.addService('_ftp', '_tcp', 21, "MicroPython", {"board": "ESP32", "service": "my_hostname FTP File transfer", "passive": "True"})
    _ = mdns.addService('_telnet', '_tcp', 23, "MicroPython", {"board": "ESP32", "service": "my_hostname Telnet REPL"})
    _ = mdns.addService('_http', '_tcp', 80, "MicroPython", {"board": "ESP32", "service": "my_hostname Web server"})
    print("Advertised locally as {}.local".format(hostname))

except OSError:
    print("Failed starting mDNS server - already started?")

# start telnet server for remote login
from network import telnet

print("start telnet server")
telnet.start(user='chenmatt', password='ilovecoding')

# fetch NTP time
from machine import RTC

print("inquire RTC time")
rtc = RTC()
rtc.ntp_sync(server="pool.ntp.org")

timeout = 10
for _ in range(timeout):
    if rtc.synced():
        break
    print("Waiting for rtc time")
    time.sleep(1)

if rtc.synced():
    print(time.strftime("%c", time.localtime()))
else:
    print("could not get NTP time")
