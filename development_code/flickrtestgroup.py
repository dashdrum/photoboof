#!/usr/bin/env python

import flickr_api
from datetime import datetime

def get_group(group_name):

	groups = flickr_api.Group.getGroups()

	print groups

	for g in groups:
		if g.name == group_name:
			return g

	return None

## Load authentication handler

AUTH_HANDLER_FILENAME = 'auth_handler'

flickr_api.set_auth_handler(AUTH_HANDLER_FILENAME)

user = flickr_api.test.login()

## Add Photo

start = datetime.now()

photo = flickr_api.upload(photo_file = "image01.jpg", title = "Tester")

duration = datetime.now() - start

print "Upload time:", duration


## Add to group

GROUP = 'Photoboof_test'

### Get group

start = datetime.now()

group = get_group(GROUP)

### Add photo

if group:
	group.addPhoto(photo = photo)
else:
	print 'no group'

duration = datetime.now() - start

print "Add to group time:", duration

