
import flickr_api
from flickr import get_photoset
from datetime import datetime
# import our Celery object
from celery import celery

# add the decorator so it knows send_email is a task
@celery.task
def upload_photo(photo_file=None):

    ## Load authentication handler

    AUTH_HANDLER_FILENAME = 'auth_handler'

    flickr_api.set_auth_handler(AUTH_HANDLER_FILENAME)

    user = flickr_api.test.login()

    ## Add Photo

    start = datetime.now()

    photo = flickr_api.upload(photo_file = photo_file, title = "Tester")

    duration = datetime.now() - start

    print "Upload time:", duration

    ## Add to album/photoset

    ALBUM = 'Test Album'

    ### Get photoset

    start = datetime.now()

    photoset = get_photoset(user,ALBUM)

    ### Add photo

    photoset.addPhoto(photo = photo)

    duration = datetime.now() - start