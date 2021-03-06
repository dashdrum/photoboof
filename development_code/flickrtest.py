#!/usr/bin/env python

import flickr_api
from flickr import get_album, get_group
from datetime import datetime

## Load authentication handler

AUTH_HANDLER_FILENAME = 'auth_handler'

flickr_api.set_auth_handler(AUTH_HANDLER_FILENAME)

user = flickr_api.test.login()

## Add Photo

start = datetime.now()

photo = flickr_api.upload(photo_file = "image01.jpg", title = "Tester", is_public=0)

duration = datetime.now() - start

print "Upload time:", duration

## Add to album

ALBUM = 'Test Album'

### Get album

start = datetime.now()

album = get_album(user,ALBUM)

### Add photo

if album:
	album.addPhoto(photo = photo)
else:
	print 'no album'

duration = datetime.now() - start

print "Add to album time:", duration

## Add to group

GROUP = 'Photoboof_test'

### Get group

start = datetime.now()

user_id = user.id

group = get_group(GROUP)

### Add photo

if group:
	group.addPhoto(photo = photo)
else:
	print 'no group'

duration = datetime.now() - start

print "Add to group time:", duration

