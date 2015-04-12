#!/usr/bin/env python

import os

gif_delay = 50 # How much time between frames in the animated gif


graphicsmagick = "gm convert -delay " + str(gif_delay) + " -loop 0 " + "image*.jpg " + "gmtest.gif"

os.system(graphicsmagick) #make the .gif

graphicsmagick = "gm montage -tile 2x -geometry 640x480+5+5 image*.jpg gmtest.jpg"

os.system(graphicsmagick) #make the montage