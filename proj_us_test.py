from board import LED
from machine import Pin, PWM, I2C, Timer
from hcsr04 import HCSR04
import time
import math
from mqttclient import MQTTClient
import network
import sys
import time

## activate iftt protocol to notify phone that motion was detected
##

# Check wifi connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ip = wlan.ifconfig()[0]
if ip == '0.0.0.0':
    print("no wifi connection")
    sys.exit()
else:
    print("connected to WiFi at IP", ip)

# Set up Adafruit connection
adafruitIoUrl = 'io.adafruit.com'
adafruitUsername = 'Maizo'
adafruitAioKey = 'aio_fYTp72iuviXLq718lFlleO4RvzuU'

# Define callback function
def sub_cb(topic, msg):
    print((topic, msg))

# Connect to Adafruit server
print("Connecting to Adafruit")
mqtt = MQTTClient(adafruitIoUrl, port='1883', user=adafruitUsername, password=adafruitAioKey)
time.sleep(0.5)
print("Connected!")

# This will set the function sub_cb to be called when mqtt.check_msg() checks
# that there is a message pending
mqtt.set_callback(sub_cb)

# Send test message
feedName = "Maizo/feeds/me100-project"
testMessage = "Object Detected"
mqtt.subscribe(feedName)


sensor = HCSR04(trigger_pin=22, echo_pin=23,echo_timeout_us=1000000)
vals = []
avg = 1000
## we can play with the minimum activation distance, the width of my doorstep is about 120cm

while str(mqtt.check_msg()) == 'None':
  distance = sensor.distance_cm()
  vals.append(distance)
  if len(vals) > 9:
      avg = sum(vals) / len(vals)
      vals.pop(0)
      print(avg)
  if avg < 5:
    mqtt.publish(feedName,testMessage)
    print("Published {} to {}.".format(testMessage,feedName))
  


## 
##
## activate LED (potentially flash)
##



# For one minute look for messages (e.g. from the Adafruit Toggle block) on your test feed:
#for i in range(0, 60):
#    mqtt.check_msg()
#    time.sleep(1)


#C6 = 1047
#FS6 = 1480
#siren = [FS6, C6]

#led_ext = Pin(27, mode=Pin.OUT)
#brightness = 0
#L1 = PWM(led_ext,freq=200,duty=0,timer=0)
#def tcb(timer):
#  global brightness
#  if brightness < len(siren):
#      brightness += 1
#  else:
#      brightness = 0

#  print(siren[brightness])
#  L1.freq(siren[brightness])
#  L1.duty(50)
  
#t1 = Timer(1)
#t1.init(period=250, mode=t1.PERIODIC, callback=tcb)

