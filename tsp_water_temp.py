#!/usr/bin/python

import time
import datetime

import Adafruit_GPIO.SPI as SPI
#import Adafruit_MAX31855.MAX31855 as MAX31855
from MAX31855 import MAX31855

from Adafruit_7Segment import SevenSegment
from Adafruit_LEDBackpack import LEDBackpack

segment = SevenSegment(address=0x72)
backpack = LEDBackpack(address=0x72)

backpack.setBrightness(1)

# Define a function to convert celsius to fahrenheit.
def c_to_f(c):
          return c * 9.0 / 5.0 + 32.0

# Raspberry Pi software SPI configuration.
CLK = 24
CS  = 23
DO  = 18
#sensor = MAX31855.MAX31855(CLK, CS, DO)
sensor = MAX31855(CLK, CS, DO)


# ===========================================================================
# Clock Example
# ===========================================================================

# Loop printing measurements every second.
while True:
  temp = sensor.readTempC()
  internal = sensor.readInternalC()

  #print 'Thermocouple: {0:0.3F}*C'.format(temp, c_to_f(temp))
  #print 'Internal: {0:0.3F}*C'.format(internal, c_to_f(internal))

  if (temp >= 100):
    segment.writeDigit(0, int(temp / 100))
  else:
    backpack.setBufferRow(0, 0)

  segment.writeDigit(1, int(temp / 10))
  segment.writeDigit(3, int(temp) % 10)
  segment.writeDigit(4, 0xC)

  # set deg
  #backpack.setBufferRow(5,1)
  segment.writeDigit(2, 0xf)

  time.sleep(1.0)

