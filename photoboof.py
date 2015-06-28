#!/usr/bin/env python

from os import listdir
import os
import time
import picamera
from datetime import datetime
from flickr import flickr_authenticate, flickr_upload
import RPi.GPIO as GPIO
from GPIOlib import wP2board
from time import sleep
import urllib2
import socket

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
def led_powerup_test():
    for runcount in range(0,3):

        for i in range(0,led_count):  ## 0 to led_count-1
            led_on(i)
        sleep(0.300)
        for i in range(led_count-1,-1,-1): ## led_count-1 to 0
            led_off(i)
        sleep(0.300)

    # for runcount in range(0,3):

    #     for i in range(0,led_count):  ## 0 to led_count-1
    #         led_on(i)
    #         sleep(0.100)
    #         led_off(i)
    #         sleep(0.100)


    # for runcount in range(0,3):

    #     for i in range(0,led_count):  ## 0 to led_count-1
    #         led_on(i)
    #         sleep(0.100)
    #         led_off(i)
    #     for i in range(led_count-1,-1,-1): ## led_count-1 to 0
    #         led_on(i)
    #         sleep(0.100)
    #         led_off(i)

    for runcount in range(0,3):

        for i in range(0,led_count):  ## 0 to led_count-1
            led_on(i)
        sleep(0.300)
        for i in range(led_count-1,-1,-1): ## led_count-1 to 0
            led_off(i)
        sleep(0.300)
      
def is_connected():
  try:
    urllib2.urlopen("http://www.google.com").close()
    return True
  except:
     pass
  return False  

def upload_montage(file_prefix):

    led_on(processing_led)  ## LED 4 - uploading

    connected = is_connected()
    if connected:
        # print "Upload to Flickr"

        try:

            flickr_authenticate()

            try:
                title = datetime(year=int(file_prefix[0:4]),
                                 month=int(file_prefix[4:6]),
                                 day=int(file_prefix[6:8]),
                                 hour=int(file_prefix[8:10]), 
                                 minute=int(file_prefix[10:12])).strftime('%B %d, %Y %I:%M %p')
            except:
                title=file_prefix

            start = datetime.now()

            flickr_upload(MONTAGE_PATH + file_prefix + "_grid.jpg",album=ALBUM,title=title)

            duration = datetime.now() - start

            # print "Upload time:", duration

            mv_command = 'mv ' + MONTAGE_PATH + file_prefix + "_grid.jpg " + UPLOADED_PATH + file_prefix + "_grid.jpg" 
            os.system(mv_command)
        except:
            # print 'Upload Failed'
            raise

    # else:
        # print "No connection - will upload later"

    led_off(processing_led)  

def photo_process():

    ## Camera setup
    camera = picamera.PiCamera()
    camera.resolution = (640,480) 
    #camera.resolution = (2592,1944)
    #camera.vflip = True
    #camera.hflip = True
    camera.saturation = 0
    camera.start_preview()

    ## Pose coundown
    print "Pose" 
    # TODO: Superimpose message: get your pose ready - will take 4 quick photos

    led_off(ready_led)
    for runcount in range(0,5):

        led_on(pose_led)
        sleep(0.300)
        led_off(pose_led)
        sleep(0.300)

    ## Taking photos
    print "Take Photos"
    file_prefix = time.strftime("%Y%m%d%H%M%S")
    led_on(take_led)  
    # TODO: Superimpose '1'
    with camera:
        try:
            for i, filename in enumerate(camera.capture_continuous(FILE_PATH + file_prefix + '{counter:02d}.jpg', 
                                         format=None, use_video_port=False, resize=None, splitter_port=0)):
                led_off(take_led)
                # TODO: Turn off superimposed number
                # print(filename)
                time.sleep(1)
                if i == PHOTO_COUNT - 1:
                    break
                led_on(take_led)
                # TODO: Superimpose i
        finally:
            camera.stop_preview()
            camera.close()

    # TODO: Display last photo taken  -  FILE_PATH + file_prefix + '04.jpg'

    led_on(processing_led) ## LED 3 - Making montage
    print "Making montage"

    ## Make animated GIF
    gm = "gm convert -delay " + str(GIF_DELAY) + " -loop 0 " + FILE_PATH + file_prefix + "*.jpg " + FILE_PATH + file_prefix + ".gif"
    os.system(gm) #make the .gif

    ## Make montage with text on the side
    # make the grid
    gm = "gm montage -tile 2x -geometry 640x480+5+5 " + FILE_PATH + file_prefix + "*.jpg " + MONTAGE_PATH + file_prefix + "_grid.jpg"
    os.system(gm) 
    # create text box
    gm ='gm convert -size 980x170 xc:#ffffff -pointsize 60 -font Arial -fill black -draw "text 30,105 \'' + EVENT + '\'" -pointsize 16 -draw "text 850,25 \'' + file_prefix + '\'" text.jpg'
    os.system(gm) 
    # spin it
    gm = 'gm convert -rotate "270>" text.jpg text.jpg'
    os.system(gm) 
    # join text and grid
    gm = 'gm montage -geometry x980+0  text.jpg -gravity west ' + MONTAGE_PATH + file_prefix + '_grid.jpg -gravity east  -resize x980 '+ MONTAGE_PATH + file_prefix + '_grid.jpg'
    os.system(gm) 
    # chop off the extra
    gm = 'gm convert ' + MONTAGE_PATH + file_prefix + '_grid.jpg -crop 1470x980+1131+0 ' + MONTAGE_PATH + file_prefix + '_grid.jpg'
    os.system(gm)  

    led_off(processing_led)

    ## Upload Montage

    upload_montage(file_prefix)

    ## Finished

    # TODO: Display GIF  -  FILE_PATH + file_prefix + ".gif"

    # Blink LEDs to show complete

    for runcount in range(0,3):

        for i in range(0,led_count):  ## 0 to led_count-1
            led_on(i)
        sleep(0.300)
        for i in range(led_count-1,-1,-1): ## led_count-1 to 0
            led_off(i)
        sleep(0.300)

    print "Done"
    # TODO: Superimpose message: Press Button to Begin

    led_on(ready_led)

def batch_upload():
    jpg_count =0
    jpg_list = []

    # print 'Checking for pending uploads'

    for e in listdir(MONTAGE_PATH):
        if e.endswith('jpg'):
            jpg_count += 1
            jpg_list.append(e[0:14])

    # print 'jpg count:', jpg_count
    # print 'jpg_list:', jpg_list

    if jpg_count > 0:
        led_on(processing_led)
        # print 'Uploading pending photos '
        print 'Please wait'

        for j in jpg_list:
            upload_montage(j)

        led_off(processing_led)

#-----------------------------------------------------------------------------#
# Constants

ALBUM = 'Test Album'
EVENT = 'Event Name Goes Here'
FILE_PATH = 'pics/'
MONTAGE_PATH = FILE_PATH + 'montages/'
UPLOADED_PATH = FILE_PATH + 'uploaded/'
GIF_DELAY = 50 
PHOTO_COUNT = 4

led_count = 4
ready_led = 0
pose_led = 1
take_led = 2
processing_led = 3
btn_pin = wP2board(5)

# Power up

## TODO: Display title card

# GPIO Setup

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

for i in range(0,led_count):
    GPIO.setup(wP2board(i),GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(btn_pin,GPIO.IN, pull_up_down=GPIO.PUD_UP)

led_powerup_test()

# Check for pending uploads

connected = is_connected()
if connected:
    batch_upload()

# Let's do this!!!!

print "Ready"
led_on(ready_led)
# TODO: Superimpose 'Press Button to Begin'

# Button loop

while True:
    GPIO.wait_for_edge(btn_pin, GPIO.FALLING)
    sleep(0.2) #debounce
    photo_process()

GPIO.cleanup()
