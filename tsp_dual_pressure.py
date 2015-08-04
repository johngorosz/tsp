#!/usr/bin/python

import time, signal, sys
import datetime, subprocess

#import Adafruit_GPIO.SPI as SPI
#import Adafruit_MAX31855.MAX31855 as MAX31855

from Adafruit_7Segment import SevenSegment
from Adafruit_LEDBackpack import LEDBackpack
from Adafruit_ADS1x15 import ADS1x15

segment = SevenSegment(address=0x71)
backpack = LEDBackpack(address=0x71)

backpack.setBrightness(15)

# Define a function to convert celsius to fahrenheit.
def c_to_f(c):
          return c * 9.0 / 5.0 + 32.0

# Raspberry Pi software SPI configuration.
CLK = 24
CS  = 23
DO  = 18
#sensor = MAX31855.MAX31855(CLK, CS, DO)

# Select the gain
# gain = 6144  # +/- 6.144V
gain = 4096  # +/- 4.096V
# gain = 2048  # +/- 2.048V
# gain = 1024  # +/- 1.024V
# gain = 512   # +/- 0.512V
# gain = 256   # +/- 0.256V

# Select the sample rate
# sps = 8    # 8 samples per second
# sps = 16   # 16 samples per second
# sps = 32   # 32 samples per second
# sps = 64   # 64 samples per second
# sps = 128  # 128 samples per second
sps = 250  # 250 samples per second
# sps = 475  # 475 samples per second
# sps = 860  # 860 samples per second

# ===========================================================================
# VDO pressure sensors
# ===========================================================================

ADS1015 = 0x00  # 12-bit ADC
adc = ADS1x15(ic=ADS1015)
led = 1

# Loop printing measurements every second.
while True:
  #temp = sensor.readTempC()
  #internal = sensor.readInternalC()
  #temp = 99

  today = datetime.datetime.now()
  #print "%s" % today.ctime()
  oil = 102.5 * ( adc.readADCSingleEnded(0, 4096, 250) / 819.2 )
  #print "oil: %.6f psi" % (oil)
  water = 102.5 * ( adc.readADCSingleEnded(1, 4096, 250) / 819.2 )
  if (oil > 80.0):
    oil = 80.0
  if (water > 80.0):
    water = 80.0
    if (led == 1):
      led = 0
    else:
      led = 1
    f = open('/sys/class/gpio/gpio21/value', 'w')
    f.write(str(led))
  else:
    f = open('/sys/class/gpio/gpio21/value', 'w')
    f.write('1')
  print "%s (%s) %.1f %.1f" % (today.ctime(), time.time(), oil, water)

  #print 'Thermocouple: {0:0.3F}*C'.format(temp, c_to_f(temp))
  #print 'Internal: {0:0.3F}*C'.format(internal, c_to_f(internal))

  #backpack.setBufferRow(0, 0)
  segment.clear()

  segment.writeDigit(0, int(oil / 10))
  segment.writeDigit(1, int(oil % 10))
  segment.writeDigit(3, int(water) / 10)
  segment.writeDigit(4, int(water) % 10)

  # set deg
  #backpack.setBufferRow(5,1)
  #segment.writeDigit(2, 0xf)

  # alarm
  

  time.sleep(1.0)

