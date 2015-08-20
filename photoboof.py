#!/usr/bin/env python

import sys
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
# import socket
import pygame
from random import randint

class Display :
    screen = None;

    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)

        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print 'Driver: {0} failed.'.format(driver)
                continue
            found = True
            break

        if not found:
            raise Exception('No suitable video driver found!')

        self.size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print "Framebuffer size: %d x %d" % (self.size[0], self.size[1])
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.display.update()

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."
        pass

    def render_text(self,message):
        font = pygame.font.Font(None, 60)
        mw, mh = font.size(message)
        text_surface = font.render(message,True, (255, 255, 0)) # Yellow Text
        sw = (self.size[0]/2) - (mw/2)
        sh = (self.size[1]/2) - (mh/2)
        self.screen.blit(text_surface, (sw, sh))
        # Update display
        pygame.display.update()

    def show_image(self,image_file):
        # Clear the screen to start
        self.screen.fill((0, 0, 0))
        # Render the image
        image = pygame.image.load(image_file).convert()
        image = pygame.transform.scale(image, (self.size[0], self.size[1]))
        self.screen.blit(image, (0,0))
        # Update display
        pygame.display.update()

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

def set_screen_available(status):
    if status:
        if os.path.isfile('block_slide_show'):
            os.remove('block_slide_show')
    else:
        open('block_slide_show','w+').close()

def screen_available():
    if os.path.isfile('block_slide_show'):
        return False
    else:
        return True

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

            flickr_upload(MONTAGE_PATH + file_prefix + "_grid.jpg",album=ALBUM,title=title, group=GROUP, is_public=0)

            duration = datetime.now() - start

            print "Upload time:", duration

            mv_command = 'mv ' + MONTAGE_PATH + file_prefix + "_grid.jpg " + UPLOADED_PATH + file_prefix + "_grid.jpg"
            os.system(mv_command)
        except:
            print 'Upload Failed'
            # raise

    # else:
        # print "No connection - will upload later"

    led_off(processing_led)

def photo_process(channel):

    set_screen_available(False)

    ## Camera setup
    camera = picamera.PiCamera()
    camera.resolution = (640,480)
    #camera.resolution = (2592,1944)
    #camera.vflip = True
    #camera.hflip = True
    camera.saturation = 0
    camera.brightness = 80
    camera.contrast = 50
    camera.start_preview()
    led_on(flash_led)

    ## Pose coundown
    print "Pose"
    # display.render_text('Get your pose ready \n will take 4 quick photos')

    led_off(ready_led)
    for runcount in range(0,5):

        led_on(pose_led)
        sleep(0.300)
        led_off(pose_led)
        sleep(0.200)

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
                time.sleep(2)
                if i == PHOTO_COUNT - 1:
                    break
                led_on(take_led)
                # TODO: Superimpose i
        finally:
            led_off(flash_led)
            camera.stop_preview()
            camera.close()

    ## Display last photo taken
    display.show_image(FILE_PATH + file_prefix + '04.jpg')
    display.render_text('Processing, please wait')

    led_on(processing_led) ## LED 3 - Making montage
    print "Making montage"

    # ## Make animated GIF
    # start = datetime.now()
    # gm = "gm convert -delay " + str(GIF_DELAY) + " -loop 0 " + FILE_PATH + file_prefix + "*.jpg " + FILE_PATH + file_prefix + ".gif"
    # os.system(gm) #make the .gif
    # duration = datetime.now() - start
    # print "GIF time:", duration

    ## Make montage with text on the side
    start = datetime.now()

    # make the grid
    gm = "gm montage -tile 2x -geometry 640x480+5+5 " + FILE_PATH + file_prefix + "*.jpg " + MONTAGE_PATH + file_prefix + "_grid.jpg"
    os.system(gm)

    # Copy grid to last_grid.jpg for display
    cp_command = 'cp ' + MONTAGE_PATH + file_prefix + "_grid.jpg " + "last_grid.jpg"
    os.system(cp_command)

    ## Display last grid
    display.show_image('last_grid.jpg')
    display.render_text('Processing, please wait')

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

    duration = datetime.now() - start
    print "Grid time:", duration

    led_off(processing_led)

    ## Upload Montage

    # print "Uploading"
    upload_montage(file_prefix)

    ## Finished

    ## Display grid
    display.show_image('last_grid.jpg')

    # Blink LEDs to show complete

    for runcount in range(0,3):

        for i in range(0,led_count):  ## 0 to led_count-1
            led_on(i)
        sleep(0.300)
        for i in range(led_count-1,-1,-1): ## led_count-1 to 0
            led_off(i)
        sleep(0.300)

    print "Done"

    ## Display grid
    display.show_image('last_grid.jpg')
    display.render_text('Press Button to Begin')

    led_on(ready_led)
    set_screen_available(True)

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

def exit_photoboof(channel):
    print "Closing Photoboof"
    led_powerup_test()
    GPIO.cleanup()
    sys.exit()

#-----------------------------------------------------------------------------#
# Constants

ALBUM = 'Dawnapadrewza 8'
GROUP = 'Dawnapadrewza2015'
EVENT = 'Dawn-A-Pa-Drew-Za #8 - 2015'
FILE_PATH = 'pics/'
MONTAGE_PATH = FILE_PATH + 'montages/'
UPLOADED_PATH = FILE_PATH + 'uploaded/'
GIF_DELAY = 50
PHOTO_COUNT = 4

led_count = 5
ready_led = 0
pose_led = 1
take_led = 2
processing_led = 3
flash_led = 4
btn_pin = wP2board(5)
btn2_pin = wP2board(6)

set_screen_available(True)

# Power up

display = Display()
display.show_image('splash1.png')
sleep(1.000)
display.show_image('splash2.png')
sleep(1.000)
display.show_image('splash3.png')
sleep(1.000)
display.show_image('splash4.png')
sleep(1.000)

# GPIO Setup

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

for i in range(0,led_count):
    GPIO.setup(wP2board(i),GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(btn_pin,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btn2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Exit program when button 2 is pushed
GPIO.add_event_detect(btn2_pin, GPIO.FALLING, callback=exit_photoboof, bouncetime=300)
# Run photo process when big button is pushed
GPIO.add_event_detect(btn_pin, GPIO.FALLING, callback=photo_process, bouncetime=300)

led_powerup_test()

# Check for pending

connected = is_connected()
if connected:
    batch_upload()

# Let's do this!!!!

print "Ready"
led_on(ready_led)

display.render_text('Press Button to Begin')


# Main loop

while True:

    ## Load filename array
    jpg_count =0
    jpg_list = []

    for e in listdir(FILE_PATH):
        if e.endswith('jpg'):
            jpg_count += 1
            jpg_list.append(e)

    ## Display 100 random pics
    if jpg_count > 0:
        for j in range(0,100):
            if screen_available():
                f = 'pics/' + jpg_list[randint(0,jpg_count-1)]
                try:
                    display.show_image(f)
                except:
                    pass
                display.render_text('Press Button to Begin')
                sleep(3.000)


