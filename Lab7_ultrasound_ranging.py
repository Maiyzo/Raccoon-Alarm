from hcsr04 import HCSR04
from machine import Pin,I2C

sensor = HCSR04(trigger_pin=22, echo_pin=23,echo_timeout_us=1000000)

try:
  while True:
    distance = sensor.distance_cm()
    print(distance)
except KeyboardInterrupt:
        pass
