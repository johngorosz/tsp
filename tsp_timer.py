#!/usr/bin/python
# tsp_timer
#
# set timer display and handle button press

import RPi.GPIO as GPIO
import time
import datetime
from Adafruit_7Segment import SevenSegment
from Adafruit_LEDBackpack import LEDBackpack

segment = SevenSegment(address=0x73)
backpack = LEDBackpack(address=0x73)

backpack.setBrightness(15)

BUTTON_GPIO = 17

# states constants
STOP = 1
RUN = 2
HOLD = 3

timer_state = STOP
last_timer_state = STOP

hold_time = 0
timer_start = datetime.datetime.now()
run_time = datetime.timedelta(0)

GPIO.setmode(GPIO.BCM)

GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

def button_down(channel):
  global timer_state, timer_start
  if timer_state == STOP:
    timer_state = RUN
    print "run"
    timer_start = datetime.datetime.now() - run_time
    segment.setColon(1)
  elif timer_state == RUN:
    timer_state = STOP
    print "stop"

def button_up(channel):
  print("Button release")

GPIO.add_event_detect(BUTTON_GPIO, GPIO.RISING, callback=button_down, bouncetime=500)
#GPIO.add_event_detect(17, GPIO.FALLING, callback=button_up, bouncetime=300)

while True:
  now = datetime.datetime.now()

  if timer_state == RUN:
    run_time = now - timer_start
  else:
    # Toggle colon
    segment.setColon(now.second % 2)              # Toggle colon at 1Hz

  minute = run_time.seconds / 60
  min_1 = int(minute / 10)
  min_2 = minute % 10
  second = run_time.seconds % 60
  sec_1 = int(second / 10)
  sec_2 = second % 10

  
  backpack.clear()
  # Set minutes
  if min_1 > 0:
    segment.writeDigit(0, min_1)     # Tens
  if min_1 + min_2 > 0:
    segment.writeDigit(1, min_2)     # Ones
  # Set minutes
  if min_1 + min_2 + sec_1 > 0:
    segment.writeDigit(3, sec_1)     # Tens

  segment.writeDigit(4, sec_2)       # Ones

  if(GPIO.input(BUTTON_GPIO) == 1):
    hold_time = hold_time + 1
  else:
    hold_time = 0

  if(hold_time == 4):
    timer_state = STOP
    timer_start = datetime.datetime.now()
    run_time = datetime.timedelta(0)
    segment.clear()
    #backpack.setBufferRow(0, 0)
    #backpack.clear()
    print "clear"

  
  # Wait one second
  time.sleep(1)


GPIO.cleanup()
