#!/usr/bin/env python

import flickr_api

def get_album(user,set_name):

	albums = user.getPhotosets()

	for a in albums:
		if a.title == set_name:
			return a

	return None


def get_group(group_name):

	groups = flickr_api.Group.getGroups()

	for g in groups:
		if g.name == group_name:
			return g

	return None

def flickr_authenticate():

	## Load authentication handler

	AUTH_HANDLER_FILENAME = 'auth_handler'

	flickr_api.set_auth_handler(AUTH_HANDLER_FILENAME)


def flickr_upload(photo_file, album=None, title=None, group=None, is_public=1):

	## upload photo

	print "Photo File:", photo_file

	photo = flickr_api.upload(photo_file = photo_file , title=title, is_public=is_public)

	## add to album/photoset

	if album:

		user = flickr_api.test.login()
		a = get_album(user,album)

		if a:
			a.addPhoto(photo = photo)

	if group:

		user = flickr_api.test.login()
		g = get_group(group)

		if g:
			g.addPhoto(photo = photo)

