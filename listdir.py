from os import listdir

import urllib2

import os
from datetime import datetime
from flickr import flickr_authenticate, flickr_upload

      
def is_connected():
  try:
    urllib2.urlopen("http://www.google.com").close()
    return True
  except:
     pass
  return False  

def upload_montage(file_prefix):

    # led_on(upload_led)  ## LED 4 - uploading

    connected = is_connected()
    print 'Connected', connected
    if connected:
        print "Upload to Flickr"

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

	        print "Upload time:", duration

	        mv_command = 'mv ' + MONTAGE_PATH + file_prefix + "_grid.jpg " + UPLOADED_PATH + file_prefix + "_grid.jpg" 
	        print mv_command
	        os.system(mv_command)
        except:
            print 'Upload Failed'
            raise

    else:
        print "No connection - will upload later"

    #led_off(upload_led)  


FILE_PATH = 'pics/'
MONTAGE_PATH = FILE_PATH + 'montages/'
UPLOADED_PATH = FILE_PATH + 'uploaded/'
ALBUM = 'Test Album'

jpg_count =0
jpg_list = []

for e in listdir(MONTAGE_PATH):
	if e.endswith('jpg'):
		jpg_count += 1
		jpg_list.append(e[0:14])

print 'jpg count:', jpg_count
print 'jpg_list:', jpg_list

for j in jpg_list:
	upload_montage(j)
