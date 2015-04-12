#!/usr/bin/env python

import flickr_api

def get_photoset(user,set_name):

	photosets = user.getPhotosets()

	for ps in photosets:
		if ps.title == set_name:
			return ps

	return None

def flickr_authenticate():

	## Load authentication handler

	AUTH_HANDLER_FILENAME = 'auth_handler'

	flickr_api.set_auth_handler(AUTH_HANDLER_FILENAME)


def flickr_upload(photo_file, album=None, title=None):

	## upload photo

	print "Photo File:", photo_file

	photo = flickr_api.upload(photo_file = photo_file , title=title )

	## add to album/photoset

	if album:

		user = flickr_api.test.login()
		photoset = get_photoset(user,album)

		if photoset:
			photoset.addPhoto(photo = photo)

