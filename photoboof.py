#!/usr/bin/env python


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

    for runcount in range(0,3):

        for i in range(0,led_count):  ## 0 to led_count-1
            led_on(i)
            sleep(0.100)
            led_off(i)
            sleep(0.100)


    for runcount in range(0,3):

        for i in range(0,led_count):  ## 0 to led_count-1
            led_on(i)
            sleep(0.100)
            led_off(i)
        for i in range(led_count-1,-1,-1): ## led_count-1 to 0
            led_on(i)
            sleep(0.100)
            led_off(i)

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

    led_on(upload_led)  ## LED 4 - uploading

    connected = is_connected()
    print 'Connected', connected
    if connected:
        print "Upload to Flickr"

        flickr_authenticate()

        try:
            title = datetime(year=int(file_prefix[0:4]),month=int(file_prefix[4:6]),day=int(file_prefix[6:8]),hour=int(file_prefix[8:10]), minute=int(file_prefix[10:12])).strftime('%B %d, %Y %I:%M &p')
        except:
            title=file_prefix

        start = datetime.now()

        try:
            flickr_upload(MONTAGE_PATH + file_prefix + "_grid.jpg",album=ALBUM,title=title)
        except:
            print 'Upload Failed'
            break  ## Does this get me out of the if statement?

        duration = datetime.now() - start

        print "Upload time:", duration

        mv_command = 'mv ' + MONTAGE_PATH + file_prefix + "_grid.jpg " + UPLOADED_PATH + file_prefix + "_grid.jpg" 
        print mv_command
        os.system(mv_command)

    else:
        print "No connection - will upload later"

    led_off(upload_led)  

def photo_process():
    camera = picamera.PiCamera()
    camera.resolution = (640,480) 
    #camera.resolution = (2592,1944)
    #camera.vflip = True
    #camera.hflip = True
    camera.saturation = 0
    camera.start_preview()


    print "Pose" 

    led_off(ready_led)
    for runcount in range(0,5):

        led_on(pose_led)
        sleep(0.300)
        led_off(pose_led)
        sleep(0.300)

    print "Take Pics"
    file_prefix = time.strftime("%Y%m%d%H%M%S")
    led_on(take_led)  
    with camera:
        try:
            for i, filename in enumerate(camera.capture_continuous(FILE_PATH + file_prefix + '{counter:02d}.jpg', 
                                         format=None, use_video_port=False, resize=None, splitter_port=0)):
                led_off(take_led)
                print(filename)
                time.sleep(1)
                if i == PHOTO_COUNT - 1:
                    break
                led_on(take_led)
        finally:
            camera.stop_preview()
            camera.close()

    led_on(upload_led) ## LED 3 - Making montage
    print "Making montages"
    # graphicsmagick = "gm convert -delay " + str(GIF_DELAY) + " -loop 0 " + FILE_PATH + file_prefix + "*.jpg " + FILE_PATH + file_prefix + ".gif"
    # os.system(graphicsmagick) #make the .gif
    graphicsmagick = "gm montage -tile 2x -geometry 640x480+5+5 " + FILE_PATH + file_prefix + "*.jpg " + MONTAGE_PATH + file_prefix + "_grid.jpg"
    os.system(graphicsmagick) #make the montage
    led_off(upload_led)

    ## Upload Montage

    upload_montage(file_prefix)

    ## Blink LEDs to show complete

    for runcount in range(0,3):

        for i in range(0,led_count):  ## 0 to led_count-1
            led_on(i)
        sleep(0.300)
        for i in range(led_count-1,-1,-1): ## led_count-1 to 0
            led_off(i)
        sleep(0.300)

    print "Done"

    led_on(ready_led)



ALBUM = 'Test Album'
FILE_PATH = 'pics/'
MONTAGE_PATH = FILE_PATH + 'montages/'
UPLOADED_PATH = FILE_PATH + 'uploaded/'
GIF_DELAY = 50 
PHOTO_COUNT = 4




led_count = 4
ready_led = 0
pose_led = 1
take_led = 2
upload_led = 3
btn_pin = wP2board(5)

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

for i in range(0,led_count):
    GPIO.setup(wP2board(i),GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(btn_pin,GPIO.IN, pull_up_down=GPIO.PUD_UP)

led_powerup_test()

print "Ready"
led_on(ready_led)

while True:
    GPIO.wait_for_edge(btn_pin, GPIO.FALLING)
    sleep(0.2) #debounce
    photo_process()

GPIO.cleanup()
