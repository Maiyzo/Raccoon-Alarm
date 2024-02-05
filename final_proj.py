from board import LED
from machine import Pin, PWM, I2C, Timer
from hcsr04 import HCSR04
from mqttclient import MQTTClient
import time
import math
import network

# initialize ultrasonic sensor
sensor = HCSR04(trigger_pin=22, echo_pin=23,echo_timeout_us=1000000)
vals = []
avg = 1000

# initialize LED
led_flash = Pin(14, mode=Pin.OUT)

# initialize speaker
C6 = 1047
FS6 = 1480
siren = [FS6, C6]
led_ext = Pin(27, mode=Pin.OUT)

# connect to adafruit
#  Check wifi connection
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



while True: 
    # This will set the LED to off as well as create an array to keep track of the distance the sensor is measuring
    led_flash(0)
    distance = sensor.distance_cm()
    time.sleep(0.05)
    vals.append(distance)
    if len(vals) > 9:
        avg = sum(vals) / len(vals)
        vals.pop(0)
        print(avg)

    # If the distance goes below 80cm, it means something has gotten close and will activate the speaker and LED   
    if avg < 80:
      mqtt.publish(feedName,testMessage)
      print("Published {} to {}.".format(testMessage,feedName))
      brightness = 0
      L1 = PWM(led_ext,freq=200,duty=0,timer=0)
      led_flash(1)
      def tcb(timer):
        global brightness
        if brightness < len(siren):
            brightness += 1
        else:
            brightness = 0     
      L1.freq(siren[brightness])
      L1.duty(50)
      t1 = Timer(1)
      t1.init(period=250, mode=t1.PERIODIC, callback=tcb)
      time.sleep(10)
      t1.deinit()
      L1.deinit()

   
