#!/usr/bin/env python


import os
import time
import picamera
from datetime import datetime
from flickr import flickr_authenticate, flickr_upload

ALBUM = 'Test Album'
FILE_PATH = 'pics/'
GIF_DELAY = 50 
PHOTO_COUNT = 4


print "Get Ready" 
camera = picamera.PiCamera()
camera.resolution = (640,480) 
#camera.resolution = (2592,1944)
#camera.vflip = True
#camera.hflip = True
camera.saturation = -100
camera.start_preview()


print "Take Pics"
file_prefix = time.strftime("%Y%m%d%H%M%S")
with camera:
    try:
        for i, filename in enumerate(camera.capture_continuous(FILE_PATH + file_prefix + '{counter:02d}.jpg', 
        	                         format=None, use_video_port=False, resize=None, splitter_port=0)):
            print(filename)
            time.sleep(1)
            if i == PHOTO_COUNT - 1:
                break
    finally:
        camera.stop_preview()


print "Making montages"
graphicsmagick = "gm convert -delay " + str(GIF_DELAY) + " -loop 0 " + FILE_PATH + file_prefix + "*.jpg " + FILE_PATH + file_prefix + ".gif"
os.system(graphicsmagick) #make the .gif
graphicsmagick = "gm montage -tile 2x -geometry 640x480+5+5 " + FILE_PATH + file_prefix + "*.jpg " + FILE_PATH + file_prefix + "_grid.jpg"
os.system(graphicsmagick) #make the montage


print "Upload to Flickr"

flickr_authenticate()

start = datetime.now()

flickr_upload(FILE_PATH + file_prefix + "_grid.jpg",album=ALBUM,title='Tester')

duration = datetime.now() - start

print "Upload time:", duration



print "Done"