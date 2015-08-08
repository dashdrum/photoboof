#!/usr/bin/env python

import sys
import os
import time
import RPi.GPIO as GPIO
from GPIOlib import wP2board
from time import sleep



def led_on(wPpin):
    try:
        GPIO.output(wP2board(wPpin),GPIO.LOW)
    except:
        pass

def led_off(wPpin):
    try:
        GPIO.output(wP2board(wPpin),GPIO.HIGH)
    except:
        pass



## led test
def led_powerup_test(yo):
    for runcount in range(0,3):

        for i in range(0,led_count):  ## 0 to led_count-1
            led_on(i)
        sleep(0.300)
        for i in range(led_count-1,-1,-1): ## led_count-1 to 0
            led_off(i)
        sleep(0.300)

    for runcount in range(0,3):

        for i in range(0,led_count):  ## 0 to led_count-1
            led_on(i)
        sleep(0.300)
        for i in range(led_count-1,-1,-1): ## led_count-1 to 0
            led_off(i)
        sleep(0.300)

def exit_photoboof(channel):
    print "Closing Photoboof"
    led_powerup_test()
    GPIO.cleanup()
    sys.exit()

#-----------------------------------------------------------------------------#
# Constants


led_count = 5
ready_led = 0
pose_led = 1
take_led = 2
processing_led = 3
flash_led = 4
btn_pin = wP2board(5)
btn2_pin = wP2board(6)

# Power up

# GPIO Setup

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

for i in range(0,led_count):
    GPIO.setup(wP2board(i),GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(btn_pin,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btn2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Exit program when button 2 is pushed
GPIO.add_event_detect(btn_pin, GPIO.FALLING, callback=led_powerup_test, bouncetime=300)
GPIO.add_event_detect(btn2_pin, GPIO.FALLING, callback=exit_photoboof, bouncetime=300)

led_powerup_test(0)


# Button loop

while True:
    led_on(ready_led)
    sleep(0.6)
    led_off(ready_led)
    sleep(0.6)


